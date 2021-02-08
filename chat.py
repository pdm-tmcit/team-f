import argparse, json
from datetime import datetime, timedelta, timezone

parser = argparse.ArgumentParser(description='JSON-LD chat and vote')
parser.add_argument('-m', '--method', type=str, help="chat | vote | parse", required=True)
parser.add_argument('-t', '--tempfile', type=str, help="template json-ld file", required=True)
parser.add_argument('-c', '--chat-message', type=str, help="chat message")
parser.add_argument('-v', '--vote-char-id', type=int)
args = parser.parse_args()

if __name__ == '__main__':
    with open(args.tempfile, 'r') as f:
        model = json.loads(f.read())
    if args.method == 'chat':
        timestamp = datetime.now().replace(tzinfo=timezone(timedelta(hours=+9))).isoformat()
        model['phaseStartTime'] = timestamp
        model['serverTimestamp'] = timestamp
        model['clientTimestamp'] = timestamp
        model['text']['@value'] = args.chat_message
        print(json.dumps(model))

    elif args.method == 'parse':
        print(model['character']['id'], model['text']['@value'])

    elif args.method == 'vote':
        model['character']['id'] = args.vote_char_id
        print(json.dumps(model))