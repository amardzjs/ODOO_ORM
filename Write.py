# ============================================
# ODOO ORM WRITE - COMPLETE GUIDE
# ============================================

from odoo import models, fields, api
from datetime import date, datetime, timedelta

class WriteExamples(models.Model):
    _name = 'write.examples'
    _description = 'Write Examples'

    name = fields.Char()
    description = fields.Text()
    price = fields.Float()
    qty = fields.Integer()
    active = fields.Boolean(default=True)
    date = fields.Date()
    datetime = fields.Datetime()
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')])
    partner_id = fields.Many2one('res.partner')
    line_ids = fields.One2many('write.line', 'parent_id')
    tag_ids = fields.Many2many('write.tag')

    # ============================================
    # 1. BASIC WRITE
    # ============================================
    def basic_write(self):
        # Get record first
        partner = self.env['res.partner'].browse(1)
        
        # Write single field
        partner.write({'name': 'New Name'})
        
        # Write multiple fields
        partner.write({
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+1234567890',
            'city': 'New York'
        })
        
        # Write on multiple records (recordset)
        partners = self.env['res.partner'].search([('customer', '=', True)])
        partners.write({'active': False})  # Updates ALL records in recordset

    # ============================================
    # 2. WRITE vs DIRECT ASSIGNMENT
    # ============================================
    def write_vs_assignment(self):
        partner = self.env['res.partner'].browse(1)
        
        # Method 1: Using write() - Explicit
        partner.write({'name': 'John'})
        
        # Method 2: Direct assignment - Pythonic (Recommended)
        partner.name = 'John'
        
        # Both trigger the same ORM logic!
        # Both respect @api.constrains, computed fields, etc.
        
        # Multiple fields - Method 1
        partner.write({
            'name': 'John',
            'email': 'john@example.com',
            'phone': '123456'
        })
        
        # Multiple fields - Method 2
        partner.name = 'John'
        partner.email = 'john@example.com'
        partner.phone = '123456'
        
        # When to use write()?
        # - When updating from a dictionary/vals
        # - When you want to be explicit
        # - In loops with dynamic fields

    # ============================================
    # 3. WRITE DIFFERENT FIELD TYPES
    # ============================================
    def write_field_types(self):
        record = self.env['write.examples'].browse(1)
        
        # Char / Text
        record.write({'name': 'Product A'})
        record.write({'description': 'Long description here...'})
        
        # Integer / Float
        record.write({'qty': 10})
        record.write({'price': 99.99})
        
        # Boolean
        record.write({'active': True})
        record.write({'active': False})
        
        # Date
        record.write({'date': date.today()})
        record.write({'date': '2024-12-31'})  # String format
        record.write({'date': fields.Date.today()})
        
        # Datetime
        record.write({'datetime': datetime.now()})
        record.write({'datetime': fields.Datetime.now()})
        record.write({'datetime': '2024-12-31 10:30:00'})
        
        # Selection
        record.write({'state': 'confirmed'})
        
        # Set to NULL/Empty
        record.write({'name': False})  # Sets to NULL
        record.write({'partner_id': False})  # Remove relation

    # ============================================
    # 4. WRITE RELATIONAL FIELDS (Many2one)
    # ============================================
    def write_many2one(self):
        order = self.env['sale.order'].browse(1)
        
        # Set Many2one by ID
        order.write({'partner_id': 5})
        
        # Set Many2one by record
        partner = self.env['res.partner'].browse(5)
        order.write({'partner_id': partner.id})
        
        # Direct assignment
        order.partner_id = partner
        
        # Remove relation (set to NULL)
        order.write({'partner_id': False})
        order.partner_id = False

    # ============================================
    # 5. WRITE ONE2MANY FIELDS
    # ============================================
    def write_one2many(self):
        order = self.env['sale.order'].browse(1)
        
        # One2many uses special commands: (0, 0, {values}), (1, id, {values}), etc.
        
        # ADD new line (Command 0)
        order.write({
            'order_line': [(0, 0, {
                'product_id': 10,
                'product_uom_qty': 2,
                'price_unit': 100.0
            })]
        })
        
        # UPDATE existing line (Command 1)
        line_id = order.order_line[0].id
        order.write({
            'order_line': [(1, line_id, {
                'product_uom_qty': 5,
                'price_unit': 150.0
            })]
        })
        
        # DELETE line (Command 2)
        order.write({
            'order_line': [(2, line_id, 0)]
        })
        
        # UNLINK line (remove relation without deleting) (Command 3)
        order.write({
            'order_line': [(3, line_id, 0)]
        })
        
        # CLEAR all lines (Command 5)
        order.write({
            'order_line': [(5, 0, 0)]
        })
        
        # REPLACE all lines (Command 6)
        order.write({
            'order_line': [(6, 0, [line_id_1, line_id_2, line_id_3])]
        })
        
        # Multiple operations at once
        order.write({
            'order_line': [
                (0, 0, {'product_id': 10, 'product_uom_qty': 1}),  # Add new
                (1, line_id, {'product_uom_qty': 3}),              # Update existing
                (2, old_line_id, 0)                                # Delete old
            ]
        })

    # ============================================
    # 6. WRITE MANY2MANY FIELDS
    # ============================================
    def write_many2many(self):
        partner = self.env['res.partner'].browse(1)
        
        # Many2many uses same commands as One2many
        
        # ADD tags (Command 4)
        partner.write({
            'category_id': [(4, tag_id, 0)]
        })
        
        # REMOVE tag (Command 3)
        partner.write({
            'category_id': [(3, tag_id, 0)]
        })
        
        # CLEAR all tags (Command 5)
        partner.write({
            'category_id': [(5, 0, 0)]
        })
        
        # REPLACE all tags (Command 6)
        partner.write({
            'category_id': [(6, 0, [1, 2, 3, 4])]
        })
        
        # Multiple operations
        partner.write({
            'category_id': [
                (4, 10, 0),  # Add tag 10
                (4, 11, 0),  # Add tag 11
                (3, 5, 0)    # Remove tag 5
            ]
        })

    # ============================================
    # 7. RELATIONAL COMMANDS REFERENCE
    # ============================================
    def relational_commands_reference(self):
        """
        One2many / Many2many Commands:
        
        (0, 0, {values})           - CREATE new record and link
        (1, id, {values})          - UPDATE linked record with id
        (2, id, 0)                 - DELETE linked record with id (from database)
        (3, id, 0)                 - UNLINK record with id (remove relation only)
        (4, id, 0)                 - LINK existing record with id
        (5, 0, 0)                  - UNLINK ALL (clear all relations)
        (6, 0, [ids])              - REPLACE all (set these ids only)
        """
        
        order = self.env['sale.order'].browse(1)
        
        # Examples:
        order.write({
            'order_line': [
                (0, 0, {'product_id': 1, 'product_uom_qty': 1}),  # Create new
                (1, 5, {'product_uom_qty': 3}),                    # Update line 5
                (2, 10, 0),                                        # Delete line 10
                (4, 15, 0),                                        # Link existing line 15
            ]
        })

    # ============================================
    # 8. WRITE WITH SEARCH
    # ============================================
    def write_with_search(self):
        # Find and update in one flow
        
        # Update single record
        partner = self.env['res.partner'].search([('email', '=', 'test@example.com')], limit=1)
        if partner:
            partner.write({'name': 'Updated Name'})
        
        # Update multiple records
        draft_orders = self.env['sale.order'].search([('state', '=', 'draft')])
        draft_orders.write({'state': 'cancel'})
        
        # Conditional update
        partners = self.env['res.partner'].search([('country_id.code', '=', 'US')])
        for partner in partners:
            if not partner.phone:
                partner.write({'phone': 'N/A'})

    # ============================================
    # 9. WRITE IN LOOPS
    # ============================================
    def write_in_loops(self):
        # ❌ BAD - Multiple write calls (slow)
        partners = self.env['res.partner'].search([])
        for partner in partners:
            partner.write({'active': True})
        
        # ✅ GOOD - Single write for all (fast)
        partners = self.env['res.partner'].search([])
        partners.write({'active': True})
        
        # When you MUST loop (different values for each record)
        products = self.env['product.product'].search([])
        for product in products:
            new_price = product.list_price * 1.1  # 10% increase
            product.write({'list_price': new_price})
        
        # Better: Use direct assignment in loops
        for product in products:
            product.list_price = product.list_price * 1.1

    # ============================================
    # 10. WRITE WITH COMPUTED FIELDS
    # ============================================
    def write_computed_fields(self):
        # You CANNOT write to computed fields (readonly by default)
        
        # ❌ This will raise error
        # order.amount_total = 1000  # amount_total is computed
        
        # ✅ Write to fields that compute depends on
        order = self.env['sale.order'].browse(1)
        order.write({
            'order_line': [(0, 0, {
                'product_id': 1,
                'product_uom_qty': 2,
                'price_unit': 100
            })]
        })
        # amount_total will auto-compute
        
        # Exception: Computed fields with store=True and inverse function
        # can be written if inverse is defined

    # ============================================
    # 11. WRITE WITH CONSTRAINTS
    # ============================================
    def write_with_constraints(self):
        # Write will trigger @api.constrains
        
        partner = self.env['res.partner'].browse(1)
        
        try:
            partner.write({'email': 'invalid-email'})
            # If there's a constraint on email format, this will raise error
        except Exception as e:
            print(f"Constraint error: {e}")
        
        # Write will also trigger onchange methods
        # Write will recompute dependent computed fields

    # ============================================
    # 12. WRITE WITH CONTEXT
    # ============================================
    def write_with_context(self):
        partner = self.env['res.partner'].browse(1)
        
        # Write with context
        partner.with_context(no_email=True).write({'name': 'John'})
        
        # Skip auto-triggers
        partner.with_context(tracking_disable=True).write({'name': 'John'})
        
        # Write as different user
        partner.with_user(user_id).write({'name': 'John'})
        
        # Write with sudo (bypass access rights)
        partner.sudo().write({'name': 'John'})

    # ============================================
    # 13. WRITE vs CREATE
    # ============================================
    def write_vs_create(self):
        # CREATE - Makes new record
        partner = self.env['res.partner'].create({
            'name': 'New Partner',
            'email': 'new@example.com'
        })
        
        # WRITE - Updates existing record
        partner.write({'phone': '123456'})
        
        # CREATE returns the new record
        # WRITE returns True (boolean)

    # ============================================
    # 14. BATCH WRITE
    # ============================================
    def batch_write(self):
        # Update multiple records with same value - EFFICIENT
        partners = self.env['res.partner'].search([('customer', '=', True)])
        partners.write({'active': True})  # Single SQL UPDATE for all
        
        # Update multiple records with different values - LESS EFFICIENT
        vals_list = [
            {'id': 1, 'name': 'Partner 1'},
            {'id': 2, 'name': 'Partner 2'},
            {'id': 3, 'name': 'Partner 3'},
        ]
        for vals in vals_list:
            partner = self.env['res.partner'].browse(vals['id'])
            partner.write({'name': vals['name']})

    # ============================================
    # 15. WRITE RETURN VALUE
    # ============================================
    def write_return_value(self):
        partner = self.env['res.partner'].browse(1)
        
        # write() returns True
        result = partner.write({'name': 'John'})
        print(result)  # True
        
        # You can check if write succeeded
        if partner.write({'name': 'John'}):
            print("Write successful")

    # ============================================
    # 16. COMMON REAL-WORLD EXAMPLES
    # ============================================
    def real_world_examples(self):
        # Example 1: Confirm sale order
        order = self.env['sale.order'].browse(1)
        order.write({'state': 'sale'})
        # Or better:
        order.action_confirm()  # Use model's method if available
        
        # Example 2: Archive inactive customers
        inactive_partners = self.env['res.partner'].search([
            ('customer', '=', True),
            ('create_date', '<', fields.Date.today() - timedelta(days=365))
        ])
        inactive_partners.write({'active': False})
        
        # Example 3: Update prices by category
        electronics = self.env['product.product'].search([
            ('categ_id.name', '=', 'Electronics')
        ])
        for product in electronics:
            product.list_price = product.list_price * 1.15  # 15% increase
        
        # Example 4: Assign salesperson to orders
        unassigned_orders = self.env['sale.order'].search([
            ('user_id', '=', False),
            ('state', '=', 'draft')
        ])
        default_user = self.env['res.users'].browse(2)
        unassigned_orders.write({'user_id': default_user.id})
        
        # Example 5: Update invoice payment terms
        invoices = self.env['account.move'].search([
            ('partner_id', '=', 10),
            ('state', '=', 'draft')
        ])
        payment_term = self.env['account.payment.term'].search([
            ('name', '=', 'Net 30')
        ], limit=1)
        invoices.write({'invoice_payment_term_id': payment_term.id})
        
        # Example 6: Bulk update with condition
        partners = self.env['res.partner'].search([])
        for partner in partners:
            if not partner.website:
                partner.website = f"https://www.{partner.name.lower().replace(' ', '')}.com"

    # ============================================
    # 17. WRITE SAFETY & VALIDATION
    # ============================================
    def write_safety(self):
        # Always check if record exists
        partner = self.env['res.partner'].search([('id', '=', 999)], limit=1)
        if partner:
            partner.write({'name': 'John'})
        else:
            print("Partner not found")
        
        # Or use browse (won't raise error if doesn't exist)
        partner = self.env['res.partner'].browse(999)
        if partner.exists():
            partner.write({'name': 'John'})
        
        # Use try-except for validation errors
        try:
            partner = self.env['res.partner'].browse(1)
            partner.write({'email': 'invalid-email'})
        except Exception as e:
            print(f"Write failed: {e}")

    # ============================================
    # 18. WRITE PERFORMANCE TIPS
    # ============================================
    def performance_tips(self):
        # ✅ GOOD - Single write for recordset
        partners = self.env['res.partner'].search([('customer', '=', True)])
        partners.write({'active': True})
        
        # ❌ BAD - Multiple writes in loop
        partners = self.env['res.partner'].search([('customer', '=', True)])
        for partner in partners:
            partner.write({'active': True})
        
        # ✅ GOOD - Direct assignment in loop when values differ
        products = self.env['product.product'].search([])
        for product in products:
            product.list_price = product.standard_price * 1.3
        
        # ❌ BAD - Writing same field multiple times
        partner.write({'name': 'John'})
        partner.write({'email': 'john@example.com'})
        partner.write({'phone': '123'})
        
        # ✅ GOOD - Write once
        partner.write({
            'name': 'John',
            'email': 'john@example.com',
            'phone': '123'
        })
        
        # ✅ GOOD - Use sudo() only when necessary
        partner.sudo().write({'name': 'John'})  # Only if access rights needed
        
        # ✅ GOOD - Disable tracking if not needed
        partner.with_context(tracking_disable=True).write({'name': 'John'})

    # ============================================
    # 19. WRITE ERRORS & TROUBLESHOOTING
    # ============================================
    def common_errors(self):
        """
        Common write() errors:
        
        1. AccessError - No write permission
           Solution: Use sudo() or check access rights
        
        2. ValidationError - Constraint violation
           Solution: Check @api.constrains, fix data
        
        3. ValueError - Wrong field type
           Solution: Check field type, convert value
        
        4. MissingError - Record doesn't exist
           Solution: Check with exists() before write
        
        5. UserError - Business logic error
           Solution: Check model's write() override
        """
        
        # Handle access error
        try:
            partner = self.env['res.partner'].browse(1)
            partner.write({'name': 'John'})
        except AccessError:
            # Try with sudo
            partner.sudo().write({'name': 'John'})
        
        # Handle validation error
        try:
            partner.write({'email': 'invalid'})
        except ValidationError as e:
            print(f"Validation failed: {e}")
        
        # Handle missing record
        partner = self.env['res.partner'].browse(9999)
        if partner.exists():
            partner.write({'name': 'John'})

    # ============================================
    # 20. WRITE WITH INHERITANCE
    # ============================================
    def write_with_inheritance(self):
        # When you override write() in your model
        
        @api.model
        def write(self, vals):
            # Custom logic before write
            if 'name' in vals:
                vals['name'] = vals['name'].upper()
            
            # Call super to do actual write
            result = super(WriteExamples, self).write(vals)
            
            # Custom logic after write
            if 'state' in vals:
                self._send_notification()
            
            return result
        
        # When calling write, your override will be triggered
        record = self.env['write.examples'].browse(1)
        record.write({'name': 'test'})  # Will be saved as 'TEST'


# ============================================
# RELATED MODEL FOR EXAMPLES
# ============================================
class WriteLine(models.Model):
    _name = 'write.line'
    
    parent_id = fields.Many2one('write.examples')
    product_id = fields.Many2one('product.product')
    qty = fields.Integer()


class WriteTag(models.Model):
    _name = 'write.tag'
    
    name = fields.Char()