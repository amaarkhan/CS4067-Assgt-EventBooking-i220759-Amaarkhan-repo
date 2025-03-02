const nodemailer = require("nodemailer");
const dotenv = require("dotenv");

dotenv.config();

const SendEmail = ({ email, userName, emailType, noOfTickets, amount }) => {
    const transporter = nodemailer.createTransport({
        port: 587,
        host: "smtp.gmail.com",
        secure: false,
        auth: {
            user: process.env.SERVICE,
            pass: process.env.ApplicationPassword,
        },
    });

    let emailBody;
    let subject;

    if (emailType === "booking_confirmation") {
        subject = "🎟️ Ticket Purchase Confirmation";

        emailBody = `
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="background-color: #007BFF; padding: 20px; text-align: center;">
                    <h1 style="color: #fff; margin: 0;">Your Ticket Purchase</h1>
                </div>
                <div style="padding: 20px; color: #333;">
                    <h2>Hi ${userName},</h2>
                    <p>Thank you for your purchase! Your tickets are confirmed.</p>
                    <p><strong>Booking Details:</strong></p>
                    <ul>
                        <li><strong>Number of Tickets:</strong> ${noOfTickets}</li>
                        <li><strong>Total Amount Paid:</strong> $${amount}</li>
                    </ul>
                    <p>We appreciate your trust in us and look forward to seeing you at the event!</p>
                    <p>Cheers,<br>The Ticketing Team</p>
                </div>
                <div style="background-color: #f9f9f9; padding: 10px 20px; text-align: center; font-size: 12px; color: #999;">
                    &copy; 2025 Ticketing Service. All rights reserved.
                </div>
            </div>
        `;
    } else {
        throw new Error("Invalid email type provided.");
    }

    const mailOptions = {
        from: process.env.SERVICE,
        to: email,
        subject,
        html: emailBody,
    };

    transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
            console.error("❌ Error sending email:", error);
        } else {
            console.log("✅ Email sent successfully:", info.response);
        }
    });
};

module.exports = {SendEmail}