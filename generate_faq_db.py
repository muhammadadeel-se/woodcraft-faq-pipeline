import json
import sqlite3

# 1. Furniture FAQs Data (35 Realistic Q&A Pairs)
faqs = [
    {
        "question": "What types of wood do you use for your furniture?",
        "answer": "We primarily use sustainably sourced solid hardwoods including American Walnut, White Oak, Teak, and Mahogany.",
        "tags": "materials, wood, sustainability"
    },
    {
        "question": "Are your wood finishes eco-friendly?",
        "answer": "Yes, all our finishes are non-toxic, low-VOC natural oils and beeswax that highlight the wood's natural grain.",
        "tags": "materials, finish, eco-friendly"
    },
    {
        "question": "How do I clean and maintain my solid wood dining table?",
        "answer": "Wipe clean with a damp microfiber cloth. Avoid harsh chemical cleaners and use coasters to prevent water rings.",
        "tags": "care, maintenance, cleaning"
    },
    {
        "question": "Can I request custom dimensions for a bookshelf?",
        "answer": "Yes! We offer custom sizing on most of our shelving units. Contact our support team with your exact measurements.",
        "tags": "customization, sizing, bookshelf"
    },
    {
        "question": "What is your standard shipping timeframe?",
        "answer": "In-stock items ship within 5 to 7 business days. Custom orders typically take 3 to 4 weeks to craft and deliver.",
        "tags": "shipping, delivery, timeframe"
    },
    {
        "question": "Do you offer white-glove delivery services?",
        "answer": "Yes, white-glove delivery including room placement and packaging removal is available at checkout for an additional fee.",
        "tags": "shipping, delivery, white-glove"
    },
    {
        "question": "What does your furniture warranty cover?",
        "answer": "Our 5-year limited warranty covers structural defects in materials and craftsmanship under normal household use.",
        "tags": "warranty, coverage, guarantee"
    },
    {
        "question": "Are color and grain variations normal in solid wood?",
        "answer": "Yes, every piece of solid wood has unique grain patterns, knots, and tonal variations, making each item truly one-of-a-kind.",
        "tags": "materials, wood, variation"
    },
    {
        "question": "Do you ship internationally?",
        "answer": "Currently, we ship nationwide within the country, with select regional international shipping available upon special request.",
        "tags": "shipping, international"
    },
    {
        "question": "How should I protect wood furniture from direct sunlight?",
        "answer": "Keep wooden furniture away from direct, prolonged sunlight to prevent fading and natural discoloration over time.",
        "tags": "care, protection, sunlight"
    },
    {
        "question": "Can I choose a different wood stain or finish?",
        "answer": "We offer multiple stain options ranging from natural clear coat to dark espresso on all customizable catalog items.",
        "tags": "customization, finish, stain"
    },
    {
        "question": "What should I do if my furniture arrives damaged?",
        "answer": "Inspect your delivery immediately. Report any transit damage to our support team within 48 hours with photos for a swift replacement.",
        "tags": "shipping, damage, returns"
    },
    {
        "question": "How do I prevent wooden drawers from sticking?",
        "answer": "Apply a small amount of beeswax or paraffin wax along the drawer slides to ensure smooth gliding.",
        "tags": "care, maintenance, drawers"
    },
    {
        "question": "Are your chairs tested for weight capacity?",
        "answer": "All dining and office chairs are rigorously tested to support up to 300 lbs safely under standard commercial and residential use.",
        "tags": "materials, quality, chairs"
    },
    {
        "question": "Do you work with reclaimed wood?",
        "answer": "Yes, our Rustic Heritage collection is built entirely from certified reclaimed structural timber with rich historical character.",
        "tags": "materials, reclaimed, rustic"
    },
    {
        "question": "Can I cancel or modify my custom furniture order?",
        "answer": "Custom orders can be modified or canceled within 48 hours of placement before production begins.",
        "tags": "customization, orders, cancellation"
    },
    {
        "question": "How do I treat minor scratches on a table surface?",
        "answer": "Minor surface scratches can often be buffed out using a matching touch-up marker and a coat of furniture paste wax.",
        "tags": "care, repair, scratches"
    },
    {
        "question": "What payment methods do you accept online?",
        "answer": "We accept major credit cards, digital wallet transfers, and secure installment payment options at checkout.",
        "tags": "shipping, payment, checkout"
    },
    {
        "question": "Do you provide assembly services for bed frames?",
        "answer": "All bed frames include comprehensive assembly instructions and hardware. Professional assembly is also available via white-glove shipping.",
        "tags": "shipping, assembly, beds"
    },
    {
        "question": "How do I store wooden leaf extensions for dining tables?",
        "answer": "Store leaf extensions flat in a climate-controlled room away from extreme humidity and temperature swings to prevent warping.",
        "tags": "care, storage, tables"
    },
    {
        "question": "Are your fabrics stain-resistant for upholstered chairs?",
        "answer": "We offer performance fabrics treated with liquid-repellent technology for families and high-traffic dining spaces.",
        "tags": "materials, fabric, upholstery"
    },
    {
        "question": "Can I request wood samples before buying a large piece?",
        "answer": "Yes, you can order a 4x4 inch wood swatch kit containing all our standard finish options on oak and walnut.",
        "tags": "customization, samples, swatches"
    },
    {
        "question": "What is the best way to handle hot mugs or plates on wooden surfaces?",
        "answer": "Always use trivets or thick cork coasters. Direct heat can cloud or damage the protective polyurethane finish.",
        "tags": "care, protection, heat"
    },
    {
        "question": "Do you offer trade discounts for interior designers?",
        "answer": "Yes, our Trade Program offers exclusive pricing, dedicated support, and custom project coordination for design professionals.",
        "tags": "customization, trade, designers"
    },
    {
        "question": "How can I track the status of my furniture delivery?",
        "answer": "Once dispatched, you will receive a tracking link via email and SMS with live courier updates.",
        "tags": "shipping, tracking, delivery"
    },
    {
        "question": "Is assembly hardware included in flat-pack items?",
        "answer": "All necessary wrenches, bolts, and fasteners are included alongside step-by-step illustrated manuals.",
        "tags": "materials, hardware, assembly"
    },
    {
        "question": "How do I clean upholstered headboards?",
        "answer": "Vacuum gently using an upholstery attachment and spot-clean with a mild water-based foam cleanser.",
        "tags": "care, cleaning, upholstery"
    },
    {
        "question": "Can I submit my own custom furniture sketches?",
        "answer": "We love bringing bespoke ideas to life. Send your concept drawings to our design desk for a personalized quote.",
        "tags": "customization, bespoke, design"
    },
    {
        "question": "What climate conditions are ideal for solid wood furniture?",
        "answer": "Maintain indoor humidity levels between 35% and 50% to prevent natural wood expansion or cracking.",
        "tags": "care, climate, environment"
    },
    {
        "question": "Do you offer a return policy on stock furniture?",
        "answer": "Stock items can be returned within 30 days in their original packaging, subject to a standard restocking fee.",
        "tags": "warranty, returns, policy"
    },
    {
        "question": "Are your glues and adhesives safe for indoor air quality?",
        "answer": "We use formaldehyde-free, CARB Phase 2 compliant wood glues to ensure pristine indoor air quality.",
        "tags": "materials, safety, indoor"
    },
    {
        "question": "How often should I apply paste wax to wooden surfaces?",
        "answer": "Applying a fresh coat of furniture paste wax every 6 to 12 months helps maintain luster and moisture resistance.",
        "tags": "care, wax, maintenance"
    },
    {
        "question": "Can corner sofas be configured with left or right returns?",
        "answer": "Many of our modular sectional sofas feature reversible chaise configurations that adapt to your room layout.",
        "tags": "customization, modular, seating"
    },
    {
        "question": "What certification do your timber suppliers hold?",
        "answer": "Our timber suppliers are certified by the Forest Stewardship Council (FSC), ensuring responsible forestry practices.",
        "tags": "materials, FSC, sustainability"
    },
    {
        "question": "How do I contact customer support for urgent delivery questions?",
        "answer": "You can reach our support team via live chat on our website or by calling our hotline Monday through Saturday.",
        "tags": "shipping, support, contact"
    }
]

# 2. Save JSON file
with open("faq.json", "w", encoding="utf-8") as f:
    json.dump(faqs, f, indent=4)
print("Saved faq.json successfully.")

# 3. SQLite Database Setup & Insert
conn = sqlite3.connect("faq.db")
cursor = conn.cursor()

# Reset table if exists
cursor.execute("DROP TABLE IF EXISTS faq")

# Create table
cursor.execute("""
    CREATE TABLE faq (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        tags TEXT
    )
""")

# Insert rows into database
for item in faqs:
    cursor.execute(
        "INSERT INTO faq (question, answer, tags) VALUES (?, ?, ?)",
        (item["question"], item["answer"], item["tags"])
    )

conn.commit()

# 4. Verify DB content with a simple query
cursor.execute("SELECT COUNT(*) FROM faq")
count = cursor.fetchone()[0]
print(f"Database setup complete! Total rows in faq.db: {count}")

conn.close()