# __manifest__.py
{
    'name': 'Employee Rewards',
    'version': '1.0',
    'summary': 'Module pour gérer les récompenses des employés',
    'description': 'Ce module permet de créer, suivre et gérer les récompenses attribuées aux employés.',
    'author': 'Tonny Razafimananatsoa',
    'category': 'Human Resources',
    'depends': ['base', 'hr'],  # On dépend du module HR pour récupérer les employés
    'data': [
        'security/ir.model.access.csv',
        'views/employee_reward_views.xml',
        'views/employee_reward_menu.xml',
        'report/report_employee_reward.xml',
        'report/report_employee_reward_template.xml',
        'report/employee_reward_zpl_report.xml',
        'report/employee_reward_zpl_template.xml',
    ],
    'installable': True,
    'application': True,
}
