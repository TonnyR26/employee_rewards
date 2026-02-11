# from odoo import http


# class EmployeeRewards(http.Controller):
#     @http.route('/employee_rewards/employee_rewards', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_rewards/employee_rewards/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_rewards.listing', {
#             'root': '/employee_rewards/employee_rewards',
#             'objects': http.request.env['employee_rewards.employee_rewards'].search([]),
#         })

#     @http.route('/employee_rewards/employee_rewards/objects/<model("employee_rewards.employee_rewards"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_rewards.object', {
#             'object': obj
#         })

