# Imports

def build_verify_otp_email(otp: str , name: str):
    return f"""
        <html>
            <body>
            <p>
                Hello {name},
            </p>
            <p>Thanks for signing up with Namma Hotel Booking Service👋</p>
            <p>Your verfication code is:</p>
            <p style="font-weight:bold; text-align:center; margin-top:30px; background-color:#ececec; padding:10px; width:max-content;margin-left:auto; margin-right:auto">{otp[0]} {otp[1]} {otp[2]} {otp[3]} {otp[4]} {otp[5]}</p>
            <p>This code will expire in 10 minutes.</p>
            <p>If you did not request this, you can safely ignore this email.</p>
            <br/>
            <p>Thank you,</p>
            <p>--Namma Team.</p>
            </body>
        </html>
    """