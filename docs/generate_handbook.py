# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    ListFlowable, ListItem, HRFlowable
)
from reportlab.platypus.flowables import KeepTogether

OUT = "FleetX_Complete_Handbook.pdf"

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name="CoverTitle", fontName="Helvetica-Bold", fontSize=34,
    alignment=TA_CENTER, textColor=colors.HexColor("#0b1220"), spaceAfter=10
))
styles.add(ParagraphStyle(
    name="CoverSubtitle", fontName="Helvetica", fontSize=15,
    alignment=TA_CENTER, textColor=colors.HexColor("#334155"), spaceAfter=6
))
styles.add(ParagraphStyle(
    name="CoverNote", fontName="Helvetica-Oblique", fontSize=11,
    alignment=TA_CENTER, textColor=colors.HexColor("#64748b")
))
styles.add(ParagraphStyle(
    name="Chapter", fontName="Helvetica-Bold", fontSize=22,
    textColor=colors.white, backColor=colors.HexColor("#0b1220"),
    spaceBefore=0, spaceAfter=16, leftIndent=8, borderPadding=(10, 10, 10, 10)
))
styles.add(ParagraphStyle(
    name="Section", fontName="Helvetica-Bold", fontSize=15,
    textColor=colors.HexColor("#0b1220"), spaceBefore=16, spaceAfter=8,
    borderColor=colors.HexColor("#38bdf8"), borderWidth=0, borderPadding=0
))
styles.add(ParagraphStyle(
    name="SubSection", fontName="Helvetica-Bold", fontSize=12.5,
    textColor=colors.HexColor("#0f172a"), spaceBefore=10, spaceAfter=6
))
styles.add(ParagraphStyle(
    name="Body", fontName="Helvetica", fontSize=10.5, leading=15.5,
    alignment=TA_JUSTIFY, textColor=colors.HexColor("#1e293b"), spaceAfter=8
))
styles.add(ParagraphStyle(
    name="BodyLeft", parent=styles["Body"], alignment=TA_LEFT
))
styles.add(ParagraphStyle(
    name="BulletBody", parent=styles["Body"], leftIndent=14, bulletIndent=2, spaceAfter=4
))
styles.add(ParagraphStyle(
    name="CodeBlock", fontName="Courier", fontSize=9, leading=13,
    backColor=colors.HexColor("#0f172a"), textColor=colors.HexColor("#38bdf8"),
    leftIndent=10, rightIndent=10, spaceBefore=6, spaceAfter=10,
    borderPadding=(8, 8, 8, 8)
))
styles.add(ParagraphStyle(
    name="Note", fontName="Helvetica-Oblique", fontSize=10, leading=14,
    backColor=colors.HexColor("#fff7e6"), textColor=colors.HexColor("#7a4a00"),
    leftIndent=8, rightIndent=8, spaceBefore=6, spaceAfter=10,
    borderPadding=(8, 8, 8, 8)
))
styles.add(ParagraphStyle(
    name="QLabel", fontName="Helvetica-Bold", fontSize=10.5,
    textColor=colors.HexColor("#0b1220"), spaceBefore=10, spaceAfter=3
))
styles.add(ParagraphStyle(
    name="ALabel", parent=styles["Body"], leftIndent=10
))

story = []


def h1(text):
    story.append(Spacer(1, 4))
    story.append(Paragraph(text, styles["Chapter"]))


def h2(text):
    story.append(Paragraph(text, styles["Section"]))
    story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#cbd5e1"), spaceAfter=6))


def h3(text):
    story.append(Paragraph(text, styles["SubSection"]))


def p(text):
    story.append(Paragraph(text, styles["Body"]))


def bullets(items):
    lst = ListFlowable(
        [ListItem(Paragraph(i, styles["BulletBody"]), bulletColor=colors.HexColor("#38bdf8")) for i in items],
        bulletType="bullet", start="circle", leftIndent=16
    )
    story.append(lst)
    story.append(Spacer(1, 4))


def code(text):
    story.append(Paragraph(text.replace("\n", "<br/>").replace(" ", "&nbsp;"), styles["CodeBlock"]))


def note(text):
    story.append(Paragraph("<b>Note:</b> " + text, styles["Note"]))


def qa(question, answer):
    story.append(Paragraph("Q: " + question, styles["QLabel"]))
    story.append(Paragraph("A: " + answer, styles["ALabel"]))


def table(header, rows, col_widths=None):
    data = [header] + rows
    t = Table(data, colWidths=col_widths, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0b1220")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))


def pagebreak():
    story.append(PageBreak())


# ============================================================
# COVER PAGE
# ============================================================
story.append(Spacer(1, 6 * cm))
story.append(Paragraph("FleetX", styles["CoverTitle"]))
story.append(Paragraph("Vehicle Rental &amp; Fleet Analytics Platform", styles["CoverSubtitle"]))
story.append(Spacer(1, 1.5 * cm))
story.append(Paragraph("The Complete Handbook", styles["CoverSubtitle"]))
story.append(Spacer(1, 3 * cm))
story.append(Paragraph(
    "Full-Stack Development (React + Spring Boot) &nbsp;|&nbsp; Security (JWT) &nbsp;|&nbsp; Data Analytics (SQL + Python)",
    styles["CoverNote"]
))
story.append(Spacer(1, 0.5 * cm))
story.append(Paragraph(
    "Written for someone starting from zero knowledge of this project.",
    styles["CoverNote"]
))
pagebreak()

# ============================================================
# CHAPTER 0: HOW TO USE THIS HANDBOOK
# ============================================================
h1("0. How to Use This Handbook / Yeh Handbook Kaise Padhein")
p("Yeh handbook is tarah banayi gayi hai ki agar tumne pehle kabhi FleetX project ke baare mein kuch nahi suna, tab bhi tum ise shuru se aakhir tak padh ke poora project samajh jaoge — jaise ki tumne khud banaya ho.")
p("Har concept ko simple bhasha mein samjhaya gaya hai. Jahan zaroori laga, technical English term ke saath Hinglish explanation bhi di gayi hai. Isse ek interview preparation guide ki tarah bhi use kar sakte ho — end mein common interview questions aur unke answers bhi diye gaye hain.")
h3("Handbook mein kya-kya hai")
bullets([
    "Chapter 1: Project kya hai aur kyun banaya",
    "Chapter 2: Tech stack — har technology ka matlab",
    "Chapter 3: Poora architecture — sab kuch kaise connect hai",
    "Chapter 4: Database design — saari tables aur unke beech connections",
    "Chapter 5: Backend — Spring Boot ka poora kaam, module by module",
    "Chapter 6: Security — JWT, password hashing, role-based access",
    "Chapter 7: Frontend — React ka poora kaam, page by page",
    "Chapter 8: Feature walkthroughs — step by step, jab user kuch karta hai toh peeche kya hota hai",
    "Chapter 9: Analytics — SQL aur Python wala data analysis part",
    "Chapter 10: Project kaise run karein apne computer par",
    "Chapter 11: Interview questions aur unke answers",
    "Chapter 12: Glossary — har technical word ka simple matlab",
])
pagebreak()

# ============================================================
# CHAPTER 1: PROJECT OVERVIEW
# ============================================================
h1("1. Project Overview — FleetX Kya Hai")

h2("1.1 Project ka Idea")
p("FleetX ek <b>vehicle rental platform</b> hai — bilkul waisa hi jaise Zoomcar ya Ola-jaisi rental companies kaam karti hain, lekin chhote scale par, seekhne ke maksad se banaya gaya hai.")
p("Simple shabdon mein: yeh ek website hai jahan koi bhi customer account banake, available cars/bikes dekh sakta hai, unhe kuch dinon ke liye book kar sakta hai, payment (simulate) kar sakta hai, aur baad mein review de sakta hai. Doosri taraf, ek <b>Admin</b> hota hai jo poore system ko manage karta hai — naye vehicles add karna, users manage karna, maintenance track karna, waghera.")

h2("1.2 Yeh Project Kyun Banaya Gaya")
p("Iska maksad teen cheezein ek saath dikhana tha:")
bullets([
    "<b>SDE / Full-Stack Development</b> — ek real-world jaisa web application banake dikhana ki tumhe frontend aur backend dono aata hai",
    "<b>Backend Security</b> — real applications mein security kaise implement hoti hai (login, encrypted passwords, permission-based access)",
    "<b>Data Analytics</b> — jo data application collect karti hai, usse SQL aur Python se analyze karke business insights nikalna",
])
note("Yeh ek 'intermediate-level' project hai — matlab beginner se thoda upar, lekin bahut complex bhi nahi. Ismein wahi cheezein hain jo real companies apne chhote internal tools mein use karti hain.")

h2("1.3 Kaun Kya Kar Sakta Hai (Roles)")
table(
    ["Role", "Kya kar sakta hai"],
    [
        ["Customer (koi bhi)", "Register/Login, vehicles dekhna aur search/filter karna, booking karna, payment karna, review dena, apni booking history dekhna aur cancel karna"],
        ["Admin", "Sab kuch jo customer kar sakta hai, plus: vehicles add/edit/delete karna, sab users manage karna (role badalna, delete karna), maintenance start/complete karna, sab bookings/revenue dekhna"],
    ],
    col_widths=[4 * cm, 11.5 * cm]
)

pagebreak()

# ============================================================
# CHAPTER 2: TECH STACK
# ============================================================
h1("2. Tech Stack — Har Technology Ka Matlab")

p("Is project mein alag-alag kaam ke liye alag-alag tools/technologies use hui hain. Yahan har ek ko simple bhasha mein samjhaya gaya hai.")

h2("2.1 Frontend (jo user dekhta hai)")
h3("React")
p("React ek JavaScript library hai jisse hum website ka <b>UI (User Interface)</b> banate hain — jo bhi screen par dikhta hai (buttons, forms, cards) woh React se bana hai. React ki sabse badi khoobi hai <b>components</b> — poori website ko chhote-chhote reusable pieces mein tod dena. Jaise ek 'VehicleCard' component ek hi baar likha, aur use har vehicle ke liye baar-baar use kiya.")
h3("React Router")
p("Normal website mein alag-alag pages (Home, Login, Admin) hote hain. <b>React Router</b> yeh decide karta hai ki browser ke address bar mein jo URL hai, uske hisaab se kaunsa page dikhana hai — bina poora page reload kiye.")
h3("Axios")
p("Axios ek tool hai jisse frontend, backend ko <b>request</b> bhejta hai — jaise 'mujhe saari vehicles ki list do' ya 'is user ko login karo'. Yeh JavaScript ke built-in 'fetch' jaisa hi hai, bas thoda aasan syntax deta hai.")

h2("2.2 Backend (jo peeche se kaam karta hai)")
h3("Java")
p("Java ek programming language hai — backend ka saara logic isi mein likha gaya hai.")
h3("Spring Boot")
p("Spring Boot, Java ke upar bana ek <b>framework</b> hai jo backend banane ka kaam bahut aasan bana deta hai. Bina Spring Boot ke, humein bahut saara repetitive/boilerplate code khud likhna padta — Spring Boot woh sab already deta hai (jaise web server chalu karna, database se connect karna).")
h3("Spring Security")
p("Yeh Spring Boot ka hi ek hissa hai jo <b>security</b> handle karta hai — login check karna, kis user ko kaunse endpoint ka access hai, yeh sab isi se control hota hai.")

h2("2.3 Database")
h3("PostgreSQL")
p("PostgreSQL (short mein 'Postgres') ek <b>database software</b> hai — yeh asli jagah hai jahan saara data (users, vehicles, bookings) permanently store hota hai, jaise ek bahut bada, organized Excel sheet.")

h2("2.4 Security Tools")
h3("JWT (JSON Web Token)")
p("JWT ek tarika hai user ko 'login rehne' ka proof dene ka, bina baar-baar password bheje. Ise Chapter 6 mein detail se samjhaya gaya hai.")
h3("BCrypt")
p("BCrypt ek algorithm hai jo password ko <b>encrypt (scramble)</b> kar deta hai save karne se pehle, taaki database dekhne wale ko bhi asli password pata na chale.")

h2("2.5 Analytics Tools")
h3("SQL")
p("SQL (Structured Query Language) woh bhasha hai jisse hum database se sawal poochte hain — jaise 'sabse zyada revenue kis mahine mein aaya'.")
h3("Python + Pandas")
p("Python ek programming language hai jo data analysis ke liye bahut popular hai. Pandas, Python ki ek library hai jo Excel-jaisi tables (data) ko handle karne mein madad karti hai.")
h3("Matplotlib")
p("Yeh Python ki library hai jisse hum charts/graphs banate hain (bar chart, pie chart waghera).")

h2("2.6 Tools")
bullets([
    "<b>Git</b> — version control tool, code ka har change track karta hai, taaki purane version par wapas ja saken",
    "<b>Postman</b> — backend ko directly test karne ka tool, bina frontend banaye",
    "<b>VS Code</b> — code likhne ka editor (IDE)",
    "<b>pgAdmin</b> — PostgreSQL database ko dekhne/manage karne ka visual tool",
])

pagebreak()

# ============================================================
# CHAPTER 3: ARCHITECTURE
# ============================================================
h1("3. Poora Architecture — Sab Kuch Kaise Connect Hai")

h2("3.1 High-Level Picture")
p("FleetX teen alag-alag hisson mein bata hai, jo ek doosre se baat karte hain:")
code("React Frontend  --------->  Spring Boot Backend  --------->  PostgreSQL Database\n(localhost:5173)         (localhost:8080)              (localhost:5432)\n\n         &lt;---------  JSON data wapas  &lt;---------")
p("<b>Frontend</b> aur <b>Backend</b> do bilkul alag programs hain, alag-alag ports par chalte hain. Woh ek doosre se sirf <b>REST API</b> ke through baat karte hain — matlab frontend, backend ko ek 'address' (jaise <font face='Courier'>/api/vehicles</font>) par request bhejta hai, backend uska jawab JSON format mein deta hai.")

h2("3.2 Backend Ke Andar 4 Layers")
p("Jab bhi koi request backend tak pahunchti hai (jaise 'mujhe vehicle id 3 ki details do'), woh 4 layers se guzarti hai — ek relay race jaisa:")
table(
    ["Layer", "Kaam"],
    [
        ["1. Controller", "'Front desk' — request ko receive karta hai, decide karta hai kaunsa Service call karna hai. Khud koi logic nahi karta."],
        ["2. Service", "'Decision maker' — asli business logic yahan hoti hai (jaise 'check karo vehicle available hai ya nahi')"],
        ["3. Repository", "'Database messenger' — sirf yehi layer database se seedha baat karti hai (data fetch/save karna)"],
        ["4. Entity", "'Blueprint' — Java class jo ek database table ko represent karti hai"],
    ],
    col_widths=[3.2 * cm, 12.3 * cm]
)
p("Request ka safar: <b>Controller &rarr; Service &rarr; Repository &rarr; Database</b>, aur jawab wapas usi raste se ulta aata hai.")

h2("3.3 Frontend Ka Structure")
table(
    ["Folder", "Kya hai"],
    [
        ["components/", "Chhote reusable pieces — Navbar, VehicleCard, LoginForm, ReviewForm, PaymentForm, Logo"],
        ["pages/", "Poore pages jo ek route (URL) par dikhte hain — HomePage, LoginPage, RegisterPage, MyBookingsPage, AdminPage"],
        ["context/", "Global memory (UserContext) — 'kaun login hai' yeh info poore app mein available rakhta hai"],
    ],
    col_widths=[3.5 * cm, 12 * cm]
)

pagebreak()

# ============================================================
# CHAPTER 4: DATABASE DESIGN
# ============================================================
h1("4. Database Design — Saari Tables")

p("FleetX ke database mein 6 tables hain. Har table ek 'Excel sheet' jaisi hai — rows (records) aur columns (fields) ke saath.")

h2("4.1 users table")
p("Har registered person (customer ya admin) ka record.")
table(
    ["Column", "Matlab"],
    [
        ["id", "Unique number, auto-generate hota hai"],
        ["name", "Poora naam"],
        ["email", "Login ke liye use hota hai, unique hona chahiye"],
        ["password", "Encrypted (BCrypt) form mein store hota hai, plain text kabhi nahi"],
        ["phone", "Contact number"],
        ["role", "CUSTOMER ya ADMIN — sirf yeh do values allowed hain"],
        ["created_at", "Account kab bana"],
    ]
)

h2("4.2 vehicles table")
p("Rent par milne wali har gaadi ka record.")
table(
    ["Column", "Matlab"],
    [
        ["id", "Unique number"],
        ["name", "Jaise 'Honda City'"],
        ["type", "CAR ya BIKE"],
        ["number_plate", "Unique registration number"],
        ["price_per_day", "Rent price"],
        ["seats", "Seats ki sankhya"],
        ["location", "Kaunse city/branch mein hai"],
        ["status", "AVAILABLE / BOOKED / MAINTENANCE — teeno mein sirf ek ho sakta hai"],
        ["image_url", "Gaadi ki photo ka internet link"],
        ["created_at", "Kab add hui"],
    ]
)
note("'status' field bahut important hai — poora booking system isi ke upar depend karta hai. Jab booking hoti hai, status BOOKED ho jata hai; cancel hone par wapas AVAILABLE.")

h2("4.3 bookings table")
p("Jab koi customer kisi vehicle ko book karta hai, ek row yahan banti hai. Yeh table users aur vehicles dono ko 'connect' karti hai.")
table(
    ["Column", "Matlab"],
    [
        ["id", "Unique booking number"],
        ["user_id", "Kis user ne book kiya (users table ki id ki taraf pointer — 'foreign key')"],
        ["vehicle_id", "Kaunsi vehicle book hui (vehicles table ki id ki taraf pointer)"],
        ["start_date, end_date", "Rental ki date range"],
        ["total_price", "Automatically calculate hota hai: din x price_per_day"],
        ["status", "ACTIVE / COMPLETED / CANCELLED"],
        ["created_at", "Booking kab hui"],
    ]
)
note("'Foreign key' ek simple concept hai — matlab yeh column doosri table ki ek row ki taraf 'ishara' karta hai, poora data dobara copy nahi karta.")

h2("4.4 payments table")
p("Har booking ke liye simulate kiya gaya payment record.")
table(
    ["Column", "Matlab"],
    [
        ["id", "Unique payment number"],
        ["booking_id", "Kaunsi booking ke liye (ek booking ka sirf ek hi payment ho sakta hai)"],
        ["amount", "Kitna paisa (booking ke total_price se liya jaata hai)"],
        ["payment_method", "CARD / UPI / CASH"],
        ["status", "SUCCESS ya FAILED (randomly simulate hota hai, 90% success)"],
        ["paid_at", "Payment ka time"],
    ]
)

h2("4.5 maintenance_logs table")
p("Jab admin kisi vehicle ko service/repair ke liye bhejta hai.")
table(
    ["Column", "Matlab"],
    [
        ["id", "Unique record number"],
        ["vehicle_id", "Kaunsi vehicle"],
        ["description", "Kya kaam hua, jaise 'oil change'"],
        ["cost", "Maintenance ka kharcha"],
        ["start_date, end_date", "Kab shuru hua, kab khatam hua (end_date khaali ho toh matlab abhi bhi maintenance chal rahi hai)"],
    ]
)

h2("4.6 reviews table")
p("Booking khatam hone ke baad customer ki di hui rating/comment.")
table(
    ["Column", "Matlab"],
    [
        ["id", "Unique review number"],
        ["user_id", "Kisne review diya"],
        ["vehicle_id", "Kaunsi vehicle ke baare mein"],
        ["booking_id", "Kaunsi booking se juda hai (ek booking ka sirf ek review ho sakta hai)"],
        ["rating", "1 se 5"],
        ["comment", "Likha hua review"],
        ["created_at", "Kab post hua"],
    ]
)

h2("4.7 Tables Kaise Connect Hain (Relationships)")
bullets([
    "Ek USER ke <b>many</b> BOOKINGS ho sakti hain",
    "Ek VEHICLE ki <b>many</b> BOOKINGS ho sakti hain",
    "Ek BOOKING ka <b>ek hi</b> PAYMENT ho sakta hai",
    "Ek VEHICLE ke <b>many</b> MAINTENANCE_LOGS ho sakte hain",
    "Ek BOOKING ka <b>ek hi</b> REVIEW ho sakta hai (double review allow nahi hai)",
])
note("Yeh 'ek se many' wala rishta database mein <b>Foreign Key constraint</b> se enforce hota hai. Isi wajah se agar kisi vehicle ki bookings hain, toh usse seedha delete nahi kar sakte — pehle uski bookings hatani padti hain, warna database error dega (yeh humne khud experience kiya tha project banate waqt).")

pagebreak()

# ============================================================
# CHAPTER 5: BACKEND EXPLAINED
# ============================================================
h1("5. Backend Explained — Module by Module")

p("Har database table ke liye humne 4 Java files banayi (Entity, Repository, Service, Controller) — jaise Chapter 3 mein samjhaya. Ab har module ko detail se dekhte hain.")

h2("5.1 User Module")
h3("Entity (User.java)")
p("Yeh Java class 'users' table ki blueprint hai. Ismein har column ke liye ek field hai (name, email, password, role, waghera). 'role' ek <b>enum</b> hai — matlab sirf CUSTOMER ya ADMIN, koi aur value allowed nahi.")
h3("Repository (UserRepository.java)")
p("Yeh sirf 3 lines ki file hai, lekin isse hume automatically <font face='Courier'>save()</font>, <font face='Courier'>findAll()</font>, <font face='Courier'>findById()</font> jaise methods mil jaate hain, bina ek bhi SQL likhe. Ek special method bhi hai: <font face='Courier'>findByEmail()</font> — Spring Boot method ke naam se khud samajh leta hai ki kya query banani hai.")
h3("Service (UserService.java)")
p("Yahan asli logic hai:")
bullets([
    "<b>registerUser()</b> — check karta hai email pehle se exist toh nahi karta, password ko BCrypt se encrypt karta hai, fir save karta hai",
    "<b>login()</b> — email se user dhoondta hai, fir uska diya hua password aur database mein saved encrypted password ko compare karta hai",
    "<b>deleteUser(), updateRole()</b> — admin ke user-management ke liye",
])
h3("Controller (UserController.java)")
table(
    ["Address (Endpoint)", "Kaam"],
    [
        ["POST /api/users/register", "Naya account banana"],
        ["POST /api/users/login", "Login karna, JWT token milta hai"],
        ["GET /api/users", "Sab users ki list (Admin only)"],
        ["DELETE /api/users/{id}", "User delete karna (Admin only)"],
        ["PUT /api/users/{id}/role", "Role badalna (Admin only)"],
    ]
)

h2("5.2 Vehicle Module")
p("Isi pattern par bana hai. Extra khaas baatein:")
bullets([
    "<b>Status management</b> — jab vehicle add hoti hai, uska status automatically 'AVAILABLE' set hota hai",
    "<b>Filter methods</b> — <font face='Courier'>findByType()</font>, <font face='Courier'>findByStatus()</font>, <font face='Courier'>findByLocation()</font> — Spring Boot ke method-naming trick se automatically bante hain",
    "<b>Delete safety</b> — agar kisi vehicle ki bookings hain, delete karne par ek clear error milta hai ('Cannot delete this vehicle — it has existing bookings') na ki ek confusing crash",
])

h2("5.3 Booking Module — Sabse Interesting")
p("Yeh module User aur Vehicle dono ko connect karta hai, aur real business logic yahan hai:")
bullets([
    "Pehle check karta hai vehicle 'AVAILABLE' hai ya nahi — nahi toh reject",
    "<font face='Courier'>ChronoUnit.DAYS.between()</font> se automatically din count karta hai",
    "<font face='Courier'>total_price = din &times; price_per_day</font> — khud calculate hota hai, customer nahi bhar sakta",
    "Booking successful hone par vehicle ka status 'BOOKED' set kar deta hai",
    "Cancel hone par vehicle wapas 'AVAILABLE' ho jaati hai",
])

h2("5.4 Payment Module")
p("Yeh <b>simulate</b> karta hai ki payment ho raha hai — koi asli bank involved nahi hai.")
bullets([
    "Booking ka total_price hi payment ka amount ban jaata hai (customer khud amount nahi de sakta, fake kam price nahi bhar sakta)",
    "<font face='Courier'>new Random().nextInt(100) &lt; 90</font> — 90% chance SUCCESS, 10% chance FAILED, jaise real payment gateway kabhi-kabhi fail hota hai",
    "Ek booking ka sirf ek hi payment ho sakta hai — dobara try karne par clear error message milta hai",
])

h2("5.5 Maintenance Module")
bullets([
    "<b>startMaintenance()</b> — ek naya log banata hai, vehicle ka status 'MAINTENANCE' kar deta hai (taaki uss waqt koi book na kar sake)",
    "<b>completeMaintenance()</b> — log mein end_date daalta hai, vehicle ko wapas 'AVAILABLE' kar deta hai",
])

h2("5.6 Review Module")
bullets([
    "Review dete waqt sirf booking_id diya jaata hai — user aur vehicle automatically usi booking se copy ho jaate hain (koi fake review nahi bana sakta kisi doosre ki booking par)",
    "Same booking par dobara review dena block hota hai",
])

pagebreak()

# ============================================================
# CHAPTER 6: SECURITY
# ============================================================
h1("6. Security — JWT, Password Hashing, Roles")

h2("6.1 Password Kabhi Plain Text Mein Kyun Nahi Rakhte")
p("Agar database hack ho jaye, aur password plain text mein ho, toh hacker seedha sabka password padh sakta hai. Isliye hum <b>BCrypt</b> use karte hain — ek 'one-way' encryption. Matlab: password ko scramble kiya ja sakta hai, lekin scrambled version se wapas asli password nikalna practically impossible hai.")
code("Register karte waqt:\npassword = passwordEncoder.encode(\"1234\")\n// database mein save hota hai: $2a$10$efrLR... (ek lamba scrambled text)\n\nLogin karte waqt:\npasswordEncoder.matches(\"1234\", savedScrambledPassword)\n// yeh 'true' ya 'false' return karta hai, kabhi bhi unscramble nahi karta")

h2("6.2 JWT (JSON Web Token) Kya Hai")
p("Socho website ek concert hai. Jab tum ticket kharido (login karo), tumhe ek <b>wristband</b> (JWT token) milta hai. Ab jab bhi tum kisi gate (endpoint) se andar jaana chaho, tumhe bas apna wristband dikhana hai — baar-baar ticket (password) dikhane ki zaroorat nahi.")
h3("Token ke andar kya hota hai")
p("Humara JWT token mein 3 cheezein hoti hain:")
bullets([
    "<b>Email</b> — yeh batata hai token kis user ka hai",
    "<b>Role</b> — CUSTOMER ya ADMIN (isi se pata chalta hai kya permission hai)",
    "<b>Expiry time</b> — 24 ghante baad token khud expire ho jata hai",
])
p("Yeh sab ek <b>secret key</b> se 'sign' (lock) kiya jata hai, taaki koi khud se fake token na bana sake.")

h3("Har Request Ke Saath Token Kaise Jaata Hai")
p("Login hone ke baad, frontend token ko <font face='Courier'>localStorage</font> mein save kar leta hai. Har request ke saath yeh header automatically bhej diya jata hai:")
code("Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ...")
p("Backend mein ek special file <b>JwtAuthFilter.java</b> hai jo <b>har request</b> pe chalta hai. Yeh header padhta hai, token verify karta hai, aur agar sahi hai toh Spring Security ko batata hai 'yeh request is user ki hai, is role ke saath'.")

h2("6.3 Role-Based Access — Kaun Kya Kar Sakta Hai")
p("Sirf login hona kaafi nahi — humne specific rules banaye hain ki kaun kaunsa endpoint use kar sakta hai:")
table(
    ["Endpoint", "Kisko Allowed Hai"],
    [
        ["GET /api/vehicles (dekhna)", "Sabko — login zaroori nahi"],
        ["POST/PUT/DELETE /api/vehicles", "Sirf ADMIN"],
        ["/api/maintenance/**", "Sirf ADMIN"],
        ["Users manage karna (list/delete/role)", "Sirf ADMIN"],
        ["Booking banana, apni history dekhna", "Koi bhi logged-in user"],
        ["Sab bookings/payments dekhna", "Sirf ADMIN"],
    ]
)
p("Yeh sab <b>SecurityConfig.java</b> file mein define hai, aisi lines ke through:")
code('.requestMatchers(HttpMethod.POST, "/api/vehicles").hasRole("ADMIN")\n.requestMatchers(HttpMethod.GET, "/api/vehicles/**").permitAll()\n.anyRequest().authenticated()')
p("Agar koi CUSTOMER admin wala endpoint hit kare, backend seedha <b>403 Forbidden</b> error de deta hai — frontend tak pahunchne se pehle hi reject ho jata hai. Yeh humne khud test karke confirm kiya tha.")

h2("6.4 Yeh Sab Kyun Zaroori Hai (Interview Point)")
note("Bina JWT/role-check ke, koi bhi Postman se seedha 'DELETE /api/vehicles/1' bhej ke koi bhi vehicle delete kar sakta tha, bina login kiye. Real apps mein yahi sabse bada security risk hota hai. FleetX mein yeh gap identify karke fix kiya gaya — pehle simple 'localStorage mein user save karo' tarika tha, baad mein proper JWT + role check add kiya gaya.")

pagebreak()

# ============================================================
# CHAPTER 7: FRONTEND EXPLAINED
# ============================================================
h1("7. Frontend Explained — Page by Page")

h2("7.1 React Ke Bunyadi Concepts")
h3("Component")
p("Ek component bas ek JavaScript function hai jo HTML-jaisa content return karta hai. Jaise:")
code('function VehicleCard({ vehicle }) {\n  return &lt;div&gt;{vehicle.name}&lt;/div&gt;;\n}')
h3("JSX")
p("Yeh HTML jaisa dikhta hai lekin asal mein JavaScript hai — isi se hum component ke andar UI likhte hain.")
h3("useState — Component Ki Memory")
p("Jab bhi kisi cheez ko 'yaad' rakhna ho (jaise form mein kya type kiya), <font face='Courier'>useState</font> use karte hain:")
code("const [email, setEmail] = useState(\"\");\n// email = current value, setEmail = ise badalne ka function")
h3("useEffect — 'Jab Page Khule Tab Yeh Karo'")
p("Jaise hi component screen par aata hai, useEffect ke andar likha code chalta hai — jaise backend se data mangwana:")
code("useEffect(() => {\n  axios.get(\"http://localhost:8080/api/vehicles\")\n    .then(res =&gt; setVehicles(res.data));\n}, []);")
h3("Props")
p("Ek component doosre component ko data 'de' sakta hai — jaise <font face='Courier'>&lt;VehicleCard vehicle={car} /&gt;</font>. Yahan 'vehicle' ek prop hai.")

h2("7.2 Context — Global Memory")
p("Normal <font face='Courier'>useState</font> sirf usi component ke andar kaam karta hai. Lekin 'kaun login hai' jaisi info poore app mein chahiye (Navbar mein naam dikhane ke liye, Booking button mein user id ke liye). Isliye <b>UserContext</b> banaya — ek shared 'notice board' jo poora app padh/likh sakta hai.")
code("const { currentUser, login, logout } = useUser();")
p("Jab login hota hai, <font face='Courier'>login(user, token)</font> call hota hai — yeh Context ke andar user ka data save karta hai, <font face='Courier'>localStorage</font> mein bhi (taaki page refresh karne par bhi login yaad rahe), aur axios ko batata hai ki har request ke saath token bhejna hai.")

h2("7.3 React Router — Pages Ke Beech Navigation")
p("Teen cheezein milke ek naya page 'wire' karti hain:")
bullets([
    "<b>Page banao</b> (jaise LoginPage.jsx)",
    "<b>Route add karo</b> App.jsx mein — <font face='Courier'>&lt;Route path=\"/login\" element={&lt;LoginPage /&gt;} /&gt;</font>",
    "<b>Navbar mein link do</b> — <font face='Courier'>&lt;Link to=\"/login\"&gt;Login&lt;/Link&gt;</font>",
])

h2("7.4 Page-by-Page Breakdown")
h3("HomePage + VehicleList")
p("Yahan hero banner aur vehicle listing hoti hai. Search box aur type-filter dropdown se list ko client-side filter kiya jata hai. Har vehicle <b>VehicleCard</b> component mein dikhti hai, jisme apna khud ka booking-form aur reviews hote hain.")
h3("RegisterPage / LoginPage")
p("Simple forms — controlled inputs (<font face='Courier'>value</font> + <font face='Courier'>onChange</font>), submit hone par axios se backend ko POST request.")
h3("MyBookingsPage")
p("Logged-in user ki saari bookings dikhata hai, har ek ke saath Cancel, Pay Now, aur Leave a Review buttons (toggle ho ke inline forms khulte hain).")
h3("AdminPage")
p("Sabse bada page — stat tiles (revenue, active bookings), Add Vehicle form, All Vehicles list (delete button), Maintenance section, Manage Users section (role dropdown + delete), All Bookings list.")

h2("7.5 Axios Se Backend Baat Karna")
p("Har jagah pattern same hai:")
code("axios.post(\"http://localhost:8080/api/bookings/user/5/vehicle/1\", {\n  startDate: \"2026-10-01\",\n  endDate: \"2026-10-03\"\n})\n.then(response =&gt; { /* success */ })\n.catch(error =&gt; { /* kuch galat hua */ });")

pagebreak()

# ============================================================
# CHAPTER 8: FEATURE WALKTHROUGHS
# ============================================================
h1("8. Feature Walkthroughs — Step by Step")

h2("8.1 Registration")
bullets([
    "User form bharta hai (name, email, password, phone)",
    "Frontend axios se <font face='Courier'>POST /api/users/register</font> bhejta hai",
    "Backend check karta hai email pehle se hai kya",
    "Password BCrypt se encrypt hota hai",
    "Role automatically 'CUSTOMER' set hota hai",
    "Database mein naya row insert hota hai",
])

h2("8.2 Login")
bullets([
    "Email/password backend ko jaata hai",
    "Backend password compare karta hai (encrypted se)",
    "Agar sahi hai, ek JWT token banta hai (email + role ke saath)",
    "Response mein user ka data aur token dono aate hain",
    "Frontend token ko localStorage mein save karta hai, aur Context update karta hai",
])

h2("8.3 Browse aur Book Karna")
bullets([
    "HomePage load hote hi GET /api/vehicles call hoti hai",
    "User search/filter use karta hai (yeh sirf frontend mein hota hai, koi extra backend call nahi)",
    "'Book Now' dabane par dates ke saath POST request jaati hai",
    "Backend check karta hai vehicle available hai, din count karta hai, price calculate karta hai",
    "Booking ban jaati hai, vehicle status 'BOOKED' ho jaata hai",
    "Frontend list ko refresh kar deta hai taaki status turant update dikhe",
])

h2("8.4 Payment Simulation")
bullets([
    "'Pay Now' dabane par method (CARD/UPI/CASH) ke saath request jaati hai",
    "Backend check karta hai is booking ka payment pehle se toh nahi hua",
    "Random simulate hota hai — 90% SUCCESS, 10% FAILED",
    "Result frontend par dikha diya jaata hai",
])

h2("8.5 Review Dena")
bullets([
    "'Leave a Review' se ek chhota form khulta hai — rating aur comment",
    "Submit hone par booking_id ke saath backend ko bheja jaata hai",
    "Backend usi booking se user aur vehicle nikal leta hai automatically",
    "VehicleCard par woh review turant dikhne lagta hai",
])

h2("8.6 Admin — Vehicle Maintenance")
bullets([
    "Admin dropdown se vehicle chunta hai, description/cost/date bharta hai",
    "Maintenance start hote hi vehicle ka status 'MAINTENANCE' ho jaata hai (booking ke liye available nahi rehta)",
    "'Mark Complete' dabane par end_date set hota hai, vehicle wapas 'AVAILABLE'",
])

h2("8.7 Admin — Users Manage Karna")
bullets([
    "Sab users ki list dikhti hai naam, email ke saath",
    "Role dropdown se CUSTOMER/ADMIN badal sakte hain",
    "Delete button se user hata sakte hain (agar uski bookings hain toh clear error milega)",
])

pagebreak()

# ============================================================
# CHAPTER 9: ANALYTICS
# ============================================================
h1("9. Analytics — SQL aur Python")

h2("9.1 SQL Queries")
p("Yeh queries seedha database par chalti hain, real business questions ka jawab dene ke liye.")

h3("Total Revenue")
code("SELECT SUM(amount) AS total_revenue\nFROM payments\nWHERE status = 'SUCCESS';")
p("Sirf successful payments ka amount jodta hai.")

h3("Sabse Popular Vehicle")
code("SELECT v.name, COUNT(b.id) AS total_bookings\nFROM vehicles v\nLEFT JOIN bookings b ON b.vehicle_id = v.id\nGROUP BY v.id, v.name\nORDER BY total_bookings DESC;")
p("<b>LEFT JOIN</b> use kiya taaki jin vehicles ki koi booking nahi hui, wo bhi 0 ke saath dikhein.")

h3("Cancellation Rate")
code("SELECT COUNT(*) FILTER (WHERE status='CANCELLED') * 100.0 / COUNT(*)\nAS cancellation_rate_pct\nFROM bookings;")
p("<font face='Courier'>FILTER (WHERE ...)</font> ek trick hai — isse hum ek hi query mein 'total count' aur 'condition wala count' dono nikal sakte hain.")

h3("Vehicle Utilization, Top Customers, Avg Booking Value")
p("Yeh sab isi tarah ki queries hain — <font face='Courier'>GROUP BY</font>, <font face='Courier'>SUM</font>, <font face='Courier'>COUNT</font> combine karke real insights nikalna. Poori list <font face='Courier'>analytics/sql/queries.sql</font> file mein hai.")

h2("9.2 Python + Pandas")
p("Yehi SQL queries Python mein bhi chalayi gayi hain, taaki data se <b>charts</b> bana sakein.")
code("engine = create_engine(\"postgresql+psycopg2://...\")\nbookings = pd.read_sql(\"SELECT * FROM bookings\", engine)\n\nbookings_per_vehicle = bookings.groupby(\"vehicle_id\").size()\nbookings_per_vehicle.plot(kind=\"bar\")\nplt.savefig(\"output/bookings_per_vehicle.png\")")
bullets([
    "<font face='Courier'>pd.read_sql()</font> — SQL query chalake result ko ek table (DataFrame) mein le aata hai",
    "<font face='Courier'>.groupby().size()</font> — SQL ke GROUP BY + COUNT jaisa",
    "<font face='Courier'>plt.savefig()</font> — chart ko image file mein save karta hai",
])
p("Yeh sab <font face='Courier'>analytics/python/analyze.py</font> file mein hai — jab bhi chahoge, dobara chalake fresh charts mil jayenge.")

pagebreak()

# ============================================================
# CHAPTER 10: RUNNING THE PROJECT
# ============================================================
h1("10. Project Kaise Chalayein")

h2("10.1 Zaroori Software")
bullets([
    "Java (JDK 21+)",
    "Node.js (npm ke saath)",
    "PostgreSQL",
    "VS Code (ya koi bhi editor)",
])

h2("10.2 Pehli Baar Setup")
bullets([
    "PostgreSQL mein 'fleetx' naam ka database banao",
    "<font face='Courier'>backend/src/main/resources/application.properties</font> file mein database ka username/password daalo",
    "Root folder mein: <font face='Courier'>npm install</font>",
    "Frontend folder mein: <font face='Courier'>cd frontend &amp;&amp; npm install</font>",
])

h2("10.3 Har Baar Chalane Ke Liye")
p("Root folder (FleetX) mein terminal khol ke bas yeh chalao:")
code("npm run dev")
p("Yeh command <b>backend aur frontend dono ek saath</b> start kar deta hai — backend <font face='Courier'>localhost:8080</font> par, frontend <font face='Courier'>localhost:5173</font> par.")
note("Yeh ek special setup hai jo humne 'concurrently' tool se banaya — normally 2 alag terminal khol ke 2 command chalane padte, ab sirf ek command se kaam ho jata hai.")

h2("10.4 Test Karne Ke Liye Login")
table(
    ["Role", "Email/Username", "Password"],
    [
        ["Admin", "admin@fleetx.com", "admin123"],
        ["Customer", "ishdeep", "1234"],
    ]
)

pagebreak()

# ============================================================
# CHAPTER 11: INTERVIEW QUESTIONS
# ============================================================
h1("11. Interview Questions &amp; Answers")

qa("Apna project ek line mein batao.",
   "FleetX ek full-stack vehicle rental platform hai jisme React frontend, Spring Boot backend, PostgreSQL database, JWT-based security, aur SQL/Python se analytics banayi hai.")

qa("Frontend aur backend kaise baat karte hain?",
   "Dono alag ports par chalte hain (frontend 5173, backend 8080). Frontend, Axios use karke backend ko REST API requests bhejta hai (GET/POST/PUT/DELETE), backend JSON format mein jawab deta hai. Do alag origins ke beech request allow karne ke liye CORS configure kiya hai.")

qa("Backend mein layers kya hain aur kyun?",
   "Controller, Service, Repository, Entity. Har layer ka ek hi kaam hai (separation of concerns) — isse code organize, testable aur maintainable rehta hai. Controller sirf request receive karta hai, Service mein logic hai, Repository database se baat karta hai.")

qa("Authentication kaise kaam karta hai?",
   "Login hone par backend ek JWT token generate karta hai jisme user ka email aur role hota hai, ek secret key se sign kiya jata hai. Frontend is token ko har request ke Authorization header mein bhejta hai. Backend ka JwtAuthFilter har request par token verify karta hai.")

qa("Password kaise secure kiya hai?",
   "BCrypt hashing algorithm se — yeh one-way encryption hai, matlab hash se wapas asli password nikalna practically impossible hai. Login ke waqt diya gaya password hash karke saved hash se compare kiya jata hai, kabhi bhi decrypt nahi kiya jata.")

qa("Role-based access kaise implement kiya?",
   "JWT token ke andar role bhi save hota hai. Spring Security ke SecurityConfig mein har endpoint ke liye rule likha hai — jaise 'POST /api/vehicles sirf ADMIN kar sakta hai'. Agar galat role try kare, 403 Forbidden milta hai, request controller tak pahunchti hi nahi.")

qa("Database mein tables ke beech relationship kaise hai?",
   "Foreign keys se — jaise bookings table mein user_id aur vehicle_id columns hain jo users aur vehicles table ki id ki taraf point karte hain. Isse data duplicate nahi hota, aur referential integrity maintain rehti hai (jaise ek vehicle delete nahi ho sakti agar uski bookings exist karti hain).")

qa("Sabse mushkil bug kya tha aur kaise fix kiya?",
   "Ek baar customer requests galti se 403 de rahi thi. Debug karne par pata chala yeh koi security logic ka bug nahi tha — Spring Boot DevTools ka hot-reload thoda stale ho gaya tha jab humne bahut saari security files ek saath edit ki. Poori tarah restart karne se fix hua. Isse yeh seekha ki har bug security-logic ka nahi hota — environment/tooling issues bhi same symptom de sakte hain, isliye systematically debug karna zaroori hai (logs padhna, ek-ek karke test karna).")

qa("Vehicle booking ka price kaise calculate hota hai?",
   "Backend khud calculate karta hai — start aur end date ke beech ke din count karke price_per_day se multiply karta hai. Frontend ya user isse manually nahi de sakta, isliye koi fake price nahi bhej sakta.")

qa("Payment 'simulate' karne ka matlab kya hai?",
   "Koi asli bank/payment gateway involved nahi hai. Hum sirf ek random number generate karte hain — 90% chance payment 'SUCCESS' hoga, 10% 'FAILED', jaise real duniya mein bhi kabhi-kabhi payment fail hota hai. Yeh sirf demonstrate karne ke liye hai ki payment flow kaisa dikhta hai.")

qa("Analytics part mein kya kiya?",
   "SQL queries likhi jo revenue, popular vehicles, cancellation rate, vehicle utilization, aur top customers nikaalti hain. Fir wahi analysis Python aur Pandas mein dobara kiya, aur Matplotlib se bar chart aur pie chart banaye jo visually data dikhate hain.")

qa("Agar aur time milta toh kya improve karte?",
   "Power BI se ek interactive dashboard banata (SQL/Python ke baad ka agla step), automated unit tests add karta, aur real file-upload se vehicle images add karne ka feature banata (abhi sirf image URL daalna padta hai).")

pagebreak()

# ============================================================
# CHAPTER 12: GLOSSARY
# ============================================================
h1("12. Glossary — Har Term Ka Simple Matlab")

glossary = [
    ("API", "Application Programming Interface — do programs ke baat karne ka tarika/address"),
    ("REST API", "Ek style of API jisme har cheez ek 'resource' hai (jaise /api/vehicles), aur GET/POST/PUT/DELETE se uspar kaam kiya jata hai"),
    ("Endpoint", "Ek specific address jahan request bheji ja sakti hai, jaise /api/users/login"),
    ("JSON", "Data ko likhne ka ek format — {\"name\": \"Aman\"} jaisa — jisse frontend/backend aasani se samajh sakein"),
    ("Component (React)", "Ek reusable piece of UI, ek JavaScript function ki tarah"),
    ("State", "Component ki 'yaadasht' — jo data badalta rehta hai (useState se manage hota hai)"),
    ("Props", "Data jo ek component doosre ko deta hai"),
    ("Context (React)", "Poore app mein shared data — bina har component ko manually pass kiye"),
    ("Entity (Spring Boot)", "Java class jo ek database table ko represent karti hai"),
    ("Repository (Spring Boot)", "Interface jo database ke saath seedha kaam karta hai"),
    ("Service (Spring Boot)", "Class jahan business logic likha jata hai"),
    ("Controller (Spring Boot)", "Class jo web requests receive karti hai"),
    ("Dependency Injection", "Spring khud zaroori objects bana ke de deta hai (@Autowired se), humein khud banana nahi padta"),
    ("JWT", "JSON Web Token — login ka encrypted 'proof', jisme user ki info hoti hai"),
    ("BCrypt", "Password ko encrypt (scramble) karne ka algorithm, one-way (wapas decode nahi ho sakta)"),
    ("CORS", "Cross-Origin Resource Sharing — browser ka security rule jo control karta hai kaunsi website kis backend ko request bhej sakti hai"),
    ("Foreign Key", "Database column jo doosri table ki row ki taraf 'point' karta hai"),
    ("CRUD", "Create, Read, Update, Delete — 4 basic operations jo har app mein hoti hain"),
    ("GROUP BY (SQL)", "Data ko groups mein baant ke, har group ka summary nikalna (jaise COUNT, SUM)"),
    ("DataFrame (Pandas)", "Python mein ek table jaisi data-structure, Excel sheet jaisi"),
    ("Hot Reload / DevTools", "Spring Boot ka feature jo code change hote hi server ko automatically restart kar deta hai, bina manually band-chalu kiye"),
    ("localStorage", "Browser ki apni storage, jahan data tab band karne ke baad bhi yaad rehta hai"),
    ("Axios", "JavaScript library jisse backend ko HTTP requests bheji jaati hain"),
    ("Environment / .env", "Configuration jaise database password, jo code se alag rakha jata hai"),
]

for term, meaning in glossary:
    story.append(Paragraph(f"<b>{term}</b> — {meaning}", styles["Body"]))

story.append(Spacer(1, 20))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0b1220")))
story.append(Spacer(1, 10))
story.append(Paragraph(
    "Yeh handbook FleetX project ki poori journey cover karti hai — planning se leke deployment-ready state tak. Isse padhne ke baad tumhe apna khud ka project confidently explain karna aa jaana chahiye.",
    styles["CoverNote"]
))

doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    topMargin=1.8 * cm, bottomMargin=1.8 * cm,
    leftMargin=2 * cm, rightMargin=2 * cm,
    title="FleetX Complete Handbook"
)
doc.build(story)
print("PDF created:", OUT)
