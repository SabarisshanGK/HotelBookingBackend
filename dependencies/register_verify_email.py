# Imports

def build_verify_otp_email(otp: str , name: str):
    return f"""
        <html>
            <body>
            <h1>
                Welcome to namma Hotel Booking App
            </h1>
            <p>
                Hello {name} 👋,
            </p>
            <p>Please verify your account to continue with us using code below:</p>
            <p style="font-weight:bold; text-align:center; margin-top:30px; background-color:#ececec; padding:10px; width:max-content;margin-left:auto; margin-right:auto">{otp[0]} {otp[1]} {otp[2]} {otp[3]} {otp[4]} {otp[5]}</p>
            <br/>
            <p>Thank you,</p>
            <p>booking app.</p>
            </body>
        </html>
    """