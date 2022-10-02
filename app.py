from bot.core import Bot, BotConfig

bot = Bot(config=BotConfig(name="Jarvis"))
bot.start_conversation(id="1")

answer = bot.message("Hola guapo")
answer = bot.message("Cómo te llamas?")
answer = bot.message("Yo soy Joan")



# for query in speech_recognition():
#     bot.message(query)
#     bot.face_detection()
#     bot.speech_detection()

# answer = bot.message("Sí")

# answer = bot.message("sube el brazo 30 grados")
# answer = bot.message("baja el brazo veinte grados")
# answer = bot.message("avanza 10 cms")
# answer = bot.message("retrocede 4 metros")

#un poco más, más, mucho más (30)

# @APP.route('/', methods=['GET'])
# def main():
#     bot = Bot(user_phone="666126203")
#     answer = bot.message(request.args.get('query'), channel="whatsapp")
#     bot.save()
#     return jsonify({
#         "code": 1,
#         "msg": answer
#     })

# if __name__ == "__main__":
#     APP.run(host="0.0.0.0", debug=True, port=5000)
