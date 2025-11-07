# ============================================
# ODOO ORM SEARCH - COMPLETE GUIDE
# ============================================

from odoo import models, fields, api

class SearchExamples(models.Model):
    _name = 'search.examples'
    _description = 'Search Examples'

    # ============================================
    # 1. BASIC SEARCH
    # ============================================
    def basic_search(self):
        # Simple search
        partners = self.env['res.partner'].search([('name', '=', 'John')])
        
        # Search with limit
        partners = self.env['res.partner'].search([('customer', '=', True)], limit=10)
        
        # Search with offset (skip first 10)
        partners = self.env['res.partner'].search([('customer', '=', True)], offset=10, limit=10)
        
        # Search with order
        partners = self.env['res.partner'].search([('customer', '=', True)], order='name ASC')
        partners = self.env['res.partner'].search([('customer', '=', True)], order='name DESC, id ASC')
        
        # Search count only
        count = self.env['res.partner'].search_count([('customer', '=', True)])
        
        # Empty domain = all records
        all_partners = self.env['res.partner'].search([])

    # ============================================
    # 2. COMPARISON OPERATORS
    # ============================================
    def comparison_operators(self):
        # Equal / Not Equal
        records = self.env['product.product'].search([('name', '=', 'Product A')])
        records = self.env['product.product'].search([('name', '!=', 'Product A')])
        
        # Greater / Less than
        records = self.env['product.product'].search([('list_price', '>', 100)])
        records = self.env['product.product'].search([('list_price', '<', 1000)])
        records = self.env['product.product'].search([('list_price', '>=', 100)])
        records = self.env['product.product'].search([('list_price', '<=', 1000)])
        
        # In / Not In
        records = self.env['res.partner'].search([('id', 'in', [1, 2, 3, 4, 5])])
        records = self.env['res.partner'].search([('id', 'not in', [1, 2, 3])])
        
        # NULL / NOT NULL
        records = self.env['res.partner'].search([('parent_id', '=', False)])  # NULL
        records = self.env['res.partner'].search([('parent_id', '!=', False)]) # NOT NULL

    # ============================================
    # 3. PATTERN MATCHING (LIKE)
    # ============================================
    def pattern_matching(self):
        # like (case-sensitive)
        partners = self.env['res.partner'].search([('name', 'like', 'John%')])      # Starts with John
        partners = self.env['res.partner'].search([('name', 'like', '%John')])      # Ends with John
        partners = self.env['res.partner'].search([('name', 'like', '%John%')])     # Contains John
        
        # ilike (case-insensitive) - MOST USED
        partners = self.env['res.partner'].search([('name', 'ilike', '%john%')])    # Contains john (any case)
        
        # =like / =ilike (exact pattern with _ and %)
        partners = self.env['res.partner'].search([('name', '=like', 'J_hn')])      # _ matches single char
        partners = self.env['res.partner'].search([('name', '=ilike', 'j__n%')])
        
        # not like / not ilike
        partners = self.env['res.partner'].search([('name', 'not like', '%test%')])
        partners = self.env['res.partner'].search([('name', 'not ilike', '%test%')])

    # ============================================
    # 4. LOGICAL OPERATORS (AND, OR, NOT)
    # ============================================
    def logical_operators(self):
        # AND (default - implicit)
        partners = self.env['res.partner'].search([
            ('customer', '=', True),
            ('active', '=', True),
            ('country_id.code', '=', 'US')
        ])
        
        # OR - use '|' prefix
        partners = self.env['res.partner'].search([
            '|',
                ('customer', '=', True),
                ('supplier', '=', True)
        ])
        
        # Multiple OR
        partners = self.env['res.partner'].search([
            '|', '|',
                ('country_id.code', '=', 'US'),
                ('country_id.code', '=', 'UK'),
                ('country_id.code', '=', 'CA')
        ])
        
        # NOT - use '!' prefix
        partners = self.env['res.partner'].search([
            '!',
                ('active', '=', False)
        ])
        
        # Complex: (A AND B) OR C
        partners = self.env['res.partner'].search([
            '|',
                '&',
                    ('customer', '=', True),
                    ('country_id.code', '=', 'US'),
                ('is_company', '=', True)
        ])
        
        # Complex: (A OR B) AND (C OR D)
        partners = self.env['res.partner'].search([
            '&',
                '|',
                    ('customer', '=', True),
                    ('supplier', '=', True),
                '|',
                    ('country_id.code', '=', 'US'),
                    ('country_id.code', '=', 'UK')
        ])

    # ============================================
    # 5. RELATIONAL FIELD SEARCHES
    # ============================================
    def relational_searches(self):
        # Many2one - by ID
        orders = self.env['sale.order'].search([('partner_id', '=', 5)])
        
        # Many2one - by related field
        orders = self.env['sale.order'].search([('partner_id.name', '=', 'John')])
        orders = self.env['sale.order'].search([('partner_id.country_id.code', '=', 'US')])
        
        # Many2one - NULL check
        orders = self.env['sale.order'].search([('partner_id', '=', False)])
        orders = self.env['sale.order'].search([('partner_id', '!=', False)])
        
        # One2many / Many2many - has records
        partners = self.env['res.partner'].search([('child_ids', '!=', False)])  # Has children
        
        # One2many / Many2many - by related field
        orders = self.env['sale.order'].search([('order_line.product_id', '=', 10)])
        partners = self.env['res.partner'].search([('category_id', 'in', [1, 2, 3])])
        
        # Parent/Child hierarchy
        partners = self.env['res.partner'].search([('id', 'child_of', 10)])   # All children of partner 10
        partners = self.env['res.partner'].search([('id', 'parent_of', 10)])  # All parents of partner 10

    # ============================================
    # 6. DATE/DATETIME SEARCHES
    # ============================================
    def date_searches(self):
        # Date comparison
        orders = self.env['sale.order'].search([('date_order', '>=', '2024-01-01')])
        orders = self.env['sale.order'].search([('date_order', '<=', '2024-12-31')])
        
        # Date range
        orders = self.env['sale.order'].search([
            ('date_order', '>=', '2024-01-01'),
            ('date_order', '<=', '2024-12-31')
        ])
        
        # Using datetime
        from datetime import datetime, timedelta
        today = fields.Date.today()
        yesterday = today - timedelta(days=1)
        orders = self.env['sale.order'].search([('date_order', '>=', yesterday)])
        
        # Last 30 days
        thirty_days_ago = fields.Date.today() - timedelta(days=30)
        orders = self.env['sale.order'].search([('date_order', '>=', thirty_days_ago)])

    # ============================================
    # 7. ADVANCED SEARCH METHODS
    # ============================================
    def advanced_methods(self):
        # search_read() - Search + Read in one call (FASTER!)
        data = self.env['res.partner'].search_read(
            domain=[('customer', '=', True)],
            fields=['name', 'email', 'phone'],
            offset=0,
            limit=10,
            order='name ASC'
        )
        # Returns: [{'id': 1, 'name': 'John', 'email': '...', 'phone': '...'}, ...]
        
        # name_search() - For autocomplete/selection
        results = self.env['res.partner'].name_search(
            name='John',
            args=[('customer', '=', True)],
            operator='ilike',
            limit=10
        )
        # Returns: [(1, 'John Doe'), (2, 'Johnny Smith'), ...]
        
        # search_count() - Just count
        count = self.env['sale.order'].search_count([('state', '=', 'draft')])

    # ============================================
    # 8. SEARCH WITH RECORDSET METHODS
    # ============================================
    def search_with_recordset_methods(self):
        # Search then filter
        partners = self.env['res.partner'].search([('customer', '=', True)])
        active_partners = partners.filtered(lambda p: p.active)
        
        # Search then sort
        partners = self.env['res.partner'].search([('customer', '=', True)])
        sorted_partners = partners.sorted(key=lambda p: p.name)
        
        # Search then map
        partners = self.env['res.partner'].search([('customer', '=', True)])
        names = partners.mapped('name')
        emails = partners.mapped('email')
        
        # Chaining
        partner_names = self.env['res.partner'].search([
            ('customer', '=', True)
        ]).filtered(lambda p: p.country_id.code == 'US').mapped('name')

    # ============================================
    # 9. COMMON REAL-WORLD EXAMPLES
    # ============================================
    def real_world_examples(self):
        # Find active customers from USA
        customers = self.env['res.partner'].search([
            ('customer', '=', True),
            ('active', '=', True),
            ('country_id.code', '=', 'US')
        ])
        
        # Find draft/sent quotations
        quotations = self.env['sale.order'].search([
            ('state', 'in', ['draft', 'sent'])
        ])
        
        # Find confirmed orders from this month
        from datetime import datetime
        first_day = datetime.now().replace(day=1).date()
        orders = self.env['sale.order'].search([
            ('state', '=', 'sale'),
            ('date_order', '>=', first_day)
        ])
        
        # Find products in specific category with price > 100
        products = self.env['product.product'].search([
            ('categ_id.name', 'ilike', 'electronics'),
            ('list_price', '>', 100),
            ('active', '=', True)
        ])
        
        # Find partners without email
        partners = self.env['res.partner'].search([
            ('email', '=', False),
            ('customer', '=', True)
        ])
        
        # Find invoices that are overdue
        today = fields.Date.today()
        invoices = self.env['account.move'].search([
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('payment_state', '!=', 'paid'),
            ('invoice_date_due', '<', today)
        ])
        
        # Check if record exists
        partner = self.env['res.partner'].search([('email', '=', 'test@example.com')], limit=1)
        if partner:
            # Record exists
            pass
        
        # Get first record
        first_order = self.env['sale.order'].search([], order='id ASC', limit=1)
        
        # Get last record
        last_order = self.env['sale.order'].search([], order='id DESC', limit=1)
        
        # Pagination
        page = 2
        page_size = 20
        orders = self.env['sale.order'].search(
            [],
            limit=page_size,
            offset=(page - 1) * page_size,
            order='date_order DESC'
        )

    # ============================================
    # 10. PERFORMANCE TIPS
    # ============================================
    def performance_tips(self):
        # ❌ BAD - Loading all records then filtering in Python
        all_partners = self.env['res.partner'].search([])
        customers = [p for p in all_partners if p.customer]
        
        # ✅ GOOD - Filter in database
        customers = self.env['res.partner'].search([('customer', '=', True)])
        
        # ❌ BAD - Multiple searches
        for partner_id in [1, 2, 3, 4, 5]:
            partner = self.env['res.partner'].search([('id', '=', partner_id)])
        
        # ✅ GOOD - Single search with 'in'
        partners = self.env['res.partner'].search([('id', 'in', [1, 2, 3, 4, 5])])
        
        # ✅ GOOD - Use search_read when you only need specific fields
        data = self.env['res.partner'].search_read(
            [('customer', '=', True)],
            ['name', 'email']
        )
        
        # ✅ GOOD - Use limit when you don't need all results
        recent_orders = self.env['sale.order'].search([], order='date_order DESC', limit=10)
        
        # ✅ GOOD - Use sudo() when needed (bypass access rights)
        all_partners = self.env['res.partner'].sudo().search([])

    # ============================================
    # 11. SECURITY & PERMISSIONS
    # ============================================
    def security_examples(self):
        # Normal search (respects access rights)
        partners = self.env['res.partner'].search([])
        
        # Sudo search (bypass access rights) - USE CAREFULLY!
        all_partners = self.env['res.partner'].sudo().search([])
        
        # With specific user
        partners = self.env['res.partner'].with_user(user_id).search([])
        
        # With company
        partners = self.env['res.partner'].with_company(company_id).search([])
        
        # With context
        partners = self.env['res.partner'].with_context(active_test=False).search([])
        # active_test=False includes archived records

    # ============================================
    # 12. SPECIAL DOMAINS
    # ============================================
    def special_domains(self):
        # Empty domain
        all_records = self.env['res.partner'].search([])
        
        # Always True domain
        all_records = self.env['res.partner'].search([(1, '=', 1)])
        
        # Always False domain (returns empty)
        no_records = self.env['res.partner'].search([(0, '=', 1)])
        
        # Include archived records
        partners = self.env['res.partner'].with_context(active_test=False).search([])