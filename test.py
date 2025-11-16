from hugchat import hugchat

chatbot = hugchat.ChatBot(cookie_path="engine/cookies.json")
id = chatbot.new_conversation()
chatbot.change_conversation(id)

response = chatbot.chat("Tell me a joke about programmers")
print(response)
