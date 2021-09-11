"""
"""
# from flask import Flask, jsonify, request
# from flask_cors import CORS

from bot import Bot

# APP = Flask(__name__)
# CORS(APP)

bot = Bot("joan")
answer = bot.message("Gipsy, ponte firme")
print(answer)
answer = bot.message("ahora salúdame")
print(answer)

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
