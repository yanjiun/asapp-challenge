#!/bin/bash

curl -s -d @test_data/create_user.json -XPOST http://localhost:8080/createUser \
    --header "Content-Type: application/json"

response = $(curl -s -d @test_data/login.json -XPOST http://localhost:8080/login \
    --header "Content-Type: application/json")

curl -s -d @test_data/message3.json -XPOST http://localhost:8080/messages \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer 2zwcwqPWqVVRHVp8wkNwuEu2OIbVX88T"

 curl -X GET http://localhost:8080/messages -d @test_data/get_message.json \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer DiKWnQ9EIE0usKgnEg7S8Rz4KCRSTZFE"