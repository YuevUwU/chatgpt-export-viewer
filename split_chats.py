import json
import os
from datetime import datetime

def split_chats(input_file='conversations.json', output_dir='chats'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        chats = json.load(f)
    
    for chat in chats:
        chat_id = chat.get('id', 'unknown')
        if 'created_at' in chat:
            try:
                date = datetime.fromisoformat(chat['created_at'].replace('Z', '+00:00'))
                date_str = date.strftime('%Y%m%d_%H%M%S')
                filename = f"{date_str}_{chat_id}.json"
            except:
                filename = f"{chat_id}.json"
        else:
            filename = f"{chat_id}.json"
        
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(chat, f, ensure_ascii=False, indent=2)
        
        print(f"Chat saved: {filename}")

if __name__ == '__main__':
    split_chats() 