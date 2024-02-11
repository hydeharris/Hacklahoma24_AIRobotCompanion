from flask import Flask, render_template, request, jsonify
import os
import json 
import whisper
import ChatBot
import Handler 

app = Flask(__name__, static_url_path='/static')

app.template_folder = os.path.abspath('template')

chatbot = ChatBot.Chatbot()
handler = Handler.Handler()

#Read the config file for the AI assistant. Provides the general theme and major restrictions for the bot. 
with open("config.json") as config_file:
    config_contents = json.load(config_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.get_json() #Recieve the inputted information from the JavaScript frontend in JSON format. 
    texts = data['background_info']
    print(texts)
    system_message = config_contents["bot_description"]
    system_message += f"You should act as a {data['background_info'][0]['role']}. You are talking to someone named {data['background_info'][1]['name']} and you should know this about them: {data['background_info'][2]['extra_info']}"
    chatbot.set_system_message(system_message)

    return " ";

@app.route('/process_talk', methods=['POST'])
def process_talk():
    data = request.get_json() #Recieve the inputted text prompt from the JavaScript frontend in JSON format. 
    texts = data['talk_response'] 
    #print(texts)
    response = chatbot.ask(texts)
    audio = chatbot.generate_audio(response)
    #print(response)
    handler.handle_response(audio)

    with open('prompts.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return jsonify(talk_response=texts)

@app.route('/upload_audio', methods=['POST'])
def process_voice():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio part in the request'}), 400
    
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'No selected audio file'}), 400
    audio_file.save('uploaded_audio.mp3')
    current_directory = os.getcwd()
    audio_file_name = "uploaded_audio.mp3"
    audio_file_path = os.path.join(current_directory, audio_file_name)
    prompt = chatbot.transcribe_audio(audio_file_path)
    print(prompt["text"])
    response = chatbot.ask(prompt['text'])
    audio = chatbot.generate_audio(response)
    handler.handle_response(audio)

    return jsonify({'message': 'Audio uploaded successfully'}), 200
   

if __name__ == '__main__':
    app.run(debug=True, port=5001)
