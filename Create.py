# ============================================
# COMPLETE CREATE EXAMPLE - Sales Order
# All field types without any search
# ============================================

order = env['sale.order'].create({
    
    # --- SIMPLE FIELDS (Direct values) ---
    'name': 'SO001',                     # Char - text field
    'date_order': '2025-11-07',          # Date field
    'note': 'Rush delivery needed',      # Text field (longer text)
    'amount_total': 2050.0,              # Float - decimal number
    'state': 'draft',                    # Selection field
    
    # --- MANY2ONE (Link to ONE existing record - just ID) ---
    'partner_id': 5,                     # Link to customer ID 5
    'user_id': 2,                        # Link to salesperson ID 2
    'company_id': 1,                     # Link to company ID 1
    'pricelist_id': 1,                   # Link to pricelist ID 1
    
    # --- ONE2MANY (CREATE new child records) ---
    # Use (0, 0, {...}) to CREATE new lines
    'order_line': [
        (0, 0, {                         # CREATE first line
            'product_id': 10,            # Many2one - laptop product ID 10
            'product_uom_qty': 2,        # Integer - quantity 2
            'price_unit': 1000.0,        # Float - price $1000
            'discount': 5.0              # Float - 5% discount
        }),
        (0, 0, {                         # CREATE second line
            'product_id': 15,            # Many2one - mouse product ID 15
            'product_uom_qty': 5,        # Quantity: 5
            'price_unit': 10.0,          # Price: $10
            'discount': 0.0              # No discount
        }),
        (0, 0, {                         # CREATE third line
            'product_id': 20,            # Keyboard product ID 20
            'product_uom_qty': 1,        # Quantity: 1
            'price_unit': 50.0           # Price: $50
        })
    ],
    
    # --- MANY2MANY (LINK to existing records) ---
    # Use (6, 0, [IDs]) to LINK to existing tags
    'tag_ids': [(6, 0, [1, 3, 7])],     # Link to tag IDs: 1, 3, 7
})

# Save to database (required in Odoo shell)
env.cr.commit()

# ============================================
# VERIFY WHAT WE CREATED
# ============================================
print(f"✅ Order Created!")
print(f"Order ID: {order.id}")
print(f"Order Name: {order.name}")
print(f"Customer ID: {order.partner_id.id}")
print(f"Customer Name: {order.partner_id.name}")
print(f"Total Lines: {len(order.order_line)}")
print(f"Amount: ${order.amount_total}")

# Loop through lines
print("\n📦 Order Lines:")
for line in order.order_line:
    print(f"  Product: {line.product_id.name}, Qty: {line.product_uom_qty}, Price: ${line.price_unit}")

# Show tags
print(f"\n🏷️ Tags: {order.tag_ids.mapped('name')}")