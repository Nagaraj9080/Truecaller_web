from flask import Flask, render_template, request, jsonify
from truecallerpy import search_phonenumber
import asyncio
import phonenumbers

def is_valid_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        return phonenumbers.is_valid_number(parsed_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False

app = Flask(__name__, template_folder="templates")
id = "a1i0U--hhlRXWkXFhHLbJRXiCLRKoWJFCYgfgotZqrsfl2JQK4NQwjpDp6x-cDrJ"


async def search_and_return(ph_no):
    valid = is_valid_phone_number(ph_no)
    try:
        result = await search_phonenumber(ph_no, 'IN', id)
        return result
    except Exception as e:
        return {"error in number": str(e),"valid_number":valid,"phone_number":ph_no}

@app.route("/", methods=["GET"])
def index():
    return render_template("truecaller.html")

@app.route("/truecaller_search", methods=["POST"])
def truecaller_search():
    phone_number = request.form.get("phone_number")
    if not phone_number:
        return jsonify({"error": "Phone number is required"})
    result = asyncio.run(search_and_return(phone_number))
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)




