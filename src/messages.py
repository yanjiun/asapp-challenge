import contextlib
import json
import datetime


def record_message(conn, sender, receiver, content):
    json_blob = translate_message_into_blob(content)
    message_id = get_message_id(conn)
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
    with contextlib.closing(conn.cursor()) as cur:
        params = (message_id, sender, receiver, json_blob, timestamp)
        cur.execute('''INSERT INTO messages(message_id, sender_id, receiver_id, metadata, timestamp) 
                            VALUES(?, ?, ?, ?, ?)''', params)
        conn.commit()

    return message_id, timestamp


def get_messages(conn, receiver, min_id, limit):
    messages = []
    with contextlib.closing(conn.cursor()) as cur:
        params = (receiver, min_id, limit)
        cur.execute('''SELECT message_id, sender_id, timestamp, metadata 
                        FROM messages WHERE receiver_id=? AND message_id >=? LIMIT ?''', params)
        rows = cur.fetchall()
        for r in rows:
            msg_obj = {
                "id": r[0],
                "sender": r[1],
                "receiver": receiver,
                "timestamp": r[2],
                "content": decode_message(r[3])
            }
            messages.append(msg_obj)

    return messages


def get_message_id(conn):
    with contextlib.closing(conn.cursor()) as cur:
        cur.execute('''SELECT MAX(message_id) FROM messages ''')
        result = cur.fetchone()
        if result[0] is not None:
            return result[0] + 1
        else:
            return 0


def translate_message_into_blob(content):
    content_generators = {
        "text": encode_text_blob,
        "image": encode_image_blob,
        "video": encode_video_blob
    }
    return content_generators[content["type"]](content)


def encode_text_blob(content):
    content_obj = {
        "type": "text",
        "metadata": {
            "text": content["text"]
        }
    }
    json_blob = json.dumps(content_obj)
    return json_blob


def encode_image_blob(content):
    content_obj = {
        "type": "image",
        "metadata": {
            "url": content["url"],
            "height": content["height"],
            "width": content["width"]
        }
    }
    json_blob = json.dumps(content_obj)
    return json_blob


def encode_video_blob(content):
    content_obj = {
        "type": "video",
        "metadata": {
            "url": content["url"],
            "source": content["source"]
        }
    }
    json_blob = json.dumps(content_obj)
    return json_blob


def decode_message(content_string):
    content_stored = json.loads(content_string)
    content_obj = {
        "type": content_stored["type"]
    }
    for k, v in content_stored["metadata"].items():
        content_obj[k] = v
    return content_obj
