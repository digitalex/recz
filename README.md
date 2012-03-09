Companybook Recz
================
A recommendation service which can recommend other companies viewed by
the same people.

Setup
-----
Recz takes as input a file with pairs of companyId, sessionId, e.g.:

    NO0000000982506379 01d3fc5d9f23e8838ad21334aeac4cd1
    NO0000000982506379 01d3fc5d9f23e8838ad21334aeac4cd1
    NO0000000952507729 23d9c7fe7fc6ec66ae9183504cdbc2f1
    NO0000000990891370 d7174e5c77eca009d8782cd6a6b76c47
    NO0000000990891370 3aa320519fe006c7b38a3edf705e7f7a

Start the server simply like this:

    ./server.py < input.txt
