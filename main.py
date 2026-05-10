import flet as ft
import database
import auth
import operations
import export_operations
import analysis

def main(page: ft.Page):
    page.title = "Vault100 - Secure Financial Engine"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#111111"
    page.window.width = 700
    page.window.height = 900
    page.padding = 0

    database.initialize_database()

    def clear_page():
        page.controls.clear()
        page.scroll = None
        page.padding = 0

    # ─────────────────────────────────────────────
    # LOGIN PAGE
    # ─────────────────────────────────────────────
    def show_login_page():
        clear_page()

        username_field = ft.TextField(
            label="Username",
            prefix_icon=ft.Icons.PERSON,
            width=280,
        )
        password_field = ft.TextField(
            label="Password",
            prefix_icon=ft.Icons.LOCK,
            password=True,
            can_reveal_password=True,
            width=280,
        )
        error_text = ft.Text("", color=ft.Colors.RED, size=13)

        def login_handler(e):
            user = auth.verify_user(username_field.value, password_field.value)
            if user:
                show_dashboard(user)
            else:
                error_text.value = "Invalid username or password."
                page.update()

        page.add(
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Container(
                                width=380,
                                padding=40,
                                bgcolor="#1E1E1E",
                                border_radius=12,
                                border=ft.border.all(1, "#333333"),
                                content=ft.Column(
                                    [
                                        ft.Icon(ft.Icons.SHIELD, size=50, color=ft.Colors.BLUE),
                                        ft.Text("Vault100", size=28, weight=ft.FontWeight.BOLD),
                                        ft.Text("Secure Financial Engine", size=13, color=ft.Colors.GREY),
                                        ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
                                        username_field,
                                        password_field,
                                        error_text,
                                        ft.ElevatedButton(
                                            "Enter the Vault",
                                            width=280,
                                            on_click=login_handler,
                                        ),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=14,
                                    tight=True,
                                ),
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            )
        )
        page.update()

    # ─────────────────────────────────────────────
    # DASHBOARD
    # ─────────────────────────────────────────────
    def show_dashboard(session):
        clear_page()
        page.scroll = ft.ScrollMode.AUTO
        page.padding = ft.padding.only(left=24, right=24, top=12, bottom=30)

        is_admin = session["role"] == "admin"

        def section_title(text):
            return ft.Text(text, size=18, weight=ft.FontWeight.BOLD)

        def styled_card(content):
            return ft.Container(
                content=content,
                padding=16,
                bgcolor="#1E1E1E",
                border_radius=10,
                border=ft.border.all(1, "#333333"),
            )

        # ── Balance ──────────────────────────────
        balance = operations.calculate_current_balance()
        balance_card = styled_card(
            ft.Column([
                ft.Text("Total Net Balance", size=13, color=ft.Colors.GREY),
                ft.Text(
                    "{:.2f} TL".format(balance),
                    size=34, weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREEN if balance >= 0 else ft.Colors.RED,
                ),
            ], spacing=4, tight=True)
        )

        # ── Add Transaction ───────────────────────
        amt_input = ft.TextField(
            label="Amount (TL)", width=130,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        type_dropdown = ft.Dropdown(
            label="Type", width=130,
            options=[
                ft.dropdown.Option("Income"),
                ft.dropdown.Option("Expense"),
            ],
        )
        cat_dropdown = ft.Dropdown(
            label="Category", width=150,
            options=[
                ft.dropdown.Option("Food"),
                ft.dropdown.Option("Rent"),
                ft.dropdown.Option("Salary"),
                ft.dropdown.Option("Bills"),
                ft.dropdown.Option("Fun"),
                ft.dropdown.Option("General"),
            ],
        )
        desc_input = ft.TextField(label="Description", width=160)
        add_msg = ft.Text("", size=12)

        def add_btn_click(e):
            add_msg.value = ""
            if not amt_input.value or not type_dropdown.value:
                add_msg.value = "Amount and Type are required."
                add_msg.color = ft.Colors.RED
                page.update()
                return
            try:
                float(amt_input.value)
            except ValueError:
                add_msg.value = "Amount must be a number."
                add_msg.color = ft.Colors.RED
                page.update()
                return

            operations.add_transaction(
                amt_input.value,
                cat_dropdown.value or "General",
                type_dropdown.value,
                desc_input.value or "Manual Entry",
                session["username"],
            )
            show_dashboard(session)

        add_section = styled_card(
            ft.Column([
                ft.Row(
                    [amt_input, type_dropdown, cat_dropdown, desc_input,
                     ft.IconButton(
                         icon=ft.Icons.ADD_CIRCLE,
                         icon_color=ft.Colors.BLUE,
                         icon_size=36,
                         tooltip="Add Transaction",
                         on_click=add_btn_click,
                     )],
                    wrap=True,
                    spacing=8,
                ),
                add_msg,
            ], spacing=6, tight=True)
        )

        # ── Transaction History ───────────────────
        history_data = operations.get_transaction_history()

        def delete_tx_handler(e):
            operations.delete_transaction(e.control.data)
            show_dashboard(session)

        tx_rows = []
        for i in history_data:
            tx_rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(i["date"], size=12)),
                ft.DataCell(ft.Text(
                    i["type"], size=12,
                    color=ft.Colors.GREEN if i["type"] == "Income" else ft.Colors.RED,
                )),
                ft.DataCell(ft.Text("{:.2f} TL".format(i["amount"]), size=12)),
                ft.DataCell(ft.Text(i["category"] or "-", size=12)),
                ft.DataCell(ft.Text(i["description"] or "-", size=12)),
                ft.DataCell(
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=ft.Colors.RED if is_admin else ft.Colors.TRANSPARENT,
                        icon_size=18,
                        data=i["id"],
                        on_click=delete_tx_handler if is_admin else None,
                        disabled=not is_admin,
                    )
                ),
            ]))

        if not tx_rows:
            tx_rows = [ft.DataRow(cells=[
                ft.DataCell(ft.Text("No transactions yet", color=ft.Colors.GREY)),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
            ])]

        history_table = styled_card(
            ft.Column([
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Date")),
                        ft.DataColumn(ft.Text("Type")),
                        ft.DataColumn(ft.Text("Amount")),
                        ft.DataColumn(ft.Text("Category")),
                        ft.DataColumn(ft.Text("Description")),
                        ft.DataColumn(ft.Text("" if not is_admin else "Del")),
                    ],
                    rows=tx_rows,
                    horizontal_margin=8,
                    column_spacing=12,
                )
            ], scroll=ft.ScrollMode.AUTO)
        )

        # ── Analysis ─────────────────────────────
        totals = analysis.get_income_vs_expense()
        cat_totals = analysis.get_category_totals()
        net = totals["Income"] - totals["Expense"]

        def mini_card(label, value, color):
            return ft.Container(
                content=ft.Column([
                    ft.Text(label, color=ft.Colors.GREY, size=12),
                    ft.Text("{:.2f} TL".format(value),
                            color=color, size=20, weight=ft.FontWeight.BOLD),
                ], tight=True, spacing=4),
                padding=16, bgcolor="#1E1E1E",
                border_radius=8, border=ft.border.all(1, "#333333"),
                expand=True,
            )

        cat_rows = [
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(cat)),
                ft.DataCell(ft.Text("{:.2f} TL".format(amt), color=ft.Colors.RED)),
            ]) for cat, amt in sorted(cat_totals.items(), key=lambda x: x[1], reverse=True)
        ] or [ft.DataRow(cells=[
            ft.DataCell(ft.Text("No expense data", color=ft.Colors.GREY)),
            ft.DataCell(ft.Text("")),
        ])]

        analysis_section = styled_card(ft.Column([
            ft.Row([
                mini_card("Total Income", totals["Income"], ft.Colors.GREEN),
                mini_card("Total Expense", totals["Expense"], ft.Colors.RED),
                mini_card("Net", net, ft.Colors.GREEN if net >= 0 else ft.Colors.RED),
            ], spacing=10),
            ft.Text("Expense by Category", size=14, color=ft.Colors.GREY),
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Category")),
                    ft.DataColumn(ft.Text("Total Spent")),
                ],
                rows=cat_rows,
                horizontal_margin=8,
                column_spacing=16,
            ),
        ], spacing=10, tight=True))

        # ── Export ────────────────────────────────
        start_field = ft.TextField(label="From (YYYY-MM-DD)", width=180, hint_text="optional")
        end_field = ft.TextField(label="To (YYYY-MM-DD)", width=180, hint_text="optional")
        export_msg = ft.Text("", size=12)

        def export_handler(e):
            path = export_operations.export_to_text(
                start_date=start_field.value or None,
                end_date=end_field.value or None,
            )
            if path:
                export_msg.value = "Saved: {}".format(path)
                export_msg.color = ft.Colors.GREEN
            else:
                export_msg.value = "Export failed."
                export_msg.color = ft.Colors.RED
            page.update()

        export_section = styled_card(ft.Column([
            ft.Row([
                start_field, end_field,
                ft.ElevatedButton("Export", icon=ft.Icons.FILE_DOWNLOAD, on_click=export_handler),
            ], spacing=10, wrap=True),
            export_msg,
        ], spacing=6, tight=True))

        # ── Admin Panel ───────────────────────────
        admin_controls = []
        if is_admin:
            all_users = auth.get_all_users()

            new_uname = ft.TextField(label="Username", width=140)
            new_pass = ft.TextField(label="Password", width=140, password=True)
            new_role = ft.Dropdown(
                label="Role", width=120,
                options=[ft.dropdown.Option("user"), ft.dropdown.Option("admin")],
            )
            add_user_msg = ft.Text("", size=12)

            def add_user_handler(e):
                if not new_uname.value or not new_pass.value or not new_role.value:
                    add_user_msg.value = "All fields required."
                    add_user_msg.color = ft.Colors.RED
                    page.update()
                    return
                success = auth.add_user(new_uname.value, new_pass.value, new_role.value)
                if success:
                    show_dashboard(session)
                else:
                    add_user_msg.value = "Username already exists."
                    add_user_msg.color = ft.Colors.RED
                    page.update()

            def del_user_handler(e):
                auth.delete_user(e.control.data)
                show_dashboard(session)

            user_rows = [
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(u["username"])),
                    ft.DataCell(ft.Text(
                        u["role"],
                        color=ft.Colors.BLUE if u["role"] == "admin" else ft.Colors.GREY,
                    )),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.PERSON_REMOVE,
                        icon_color=ft.Colors.RED,
                        icon_size=18,
                        data=u["username"],
                        on_click=del_user_handler,
                        disabled=(
                            u["username"] == session["username"] or
                            u["role"] == "admin"
                        ),
                    )),
                ]) for u in all_users
            ]

            admin_controls = [
                ft.Divider(height=1, thickness=1),
                section_title("Admin — User Management"),
                styled_card(ft.Column([
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Username")),
                            ft.DataColumn(ft.Text("Role")),
                            ft.DataColumn(ft.Text("Remove")),
                        ],
                        rows=user_rows,
                        horizontal_margin=8,
                        column_spacing=16,
                    ),
                    ft.Divider(height=1),
                    ft.Text("Add New User", size=13, color=ft.Colors.GREY),
                    ft.Row([new_uname, new_pass, new_role,
                            ft.ElevatedButton("Add", on_click=add_user_handler)],
                           spacing=8, wrap=True),
                    add_user_msg,
                ], spacing=10, tight=True)),
            ]

        # ── Footer ────────────────────────────────
        footer = ft.Row([
            ft.Row([
                ft.Icon(ft.Icons.PERSON, size=15, color=ft.Colors.GREY),
                ft.Text(
                    "{} ({})".format(session["username"], session["role"]),
                    color=ft.Colors.GREY, size=12,
                ),
            ], spacing=4),
            ft.TextButton("Logout", on_click=lambda _: show_login_page()),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # ── Assemble ──────────────────────────────
        content = [
            ft.Text("Vault100 Dashboard", size=26, weight=ft.FontWeight.BOLD),
            balance_card,
            ft.Divider(height=1, thickness=1),
            section_title("Quick Add"),
            add_section,
            ft.Divider(height=1, thickness=1),
            section_title("Transaction History"),
            history_table,
            ft.Divider(height=1, thickness=1),
            section_title("Analysis"),
            analysis_section,
            ft.Divider(height=1, thickness=1),
            section_title("Export Statement"),
            export_section,
            *admin_controls,
            ft.Divider(height=1, thickness=1),
            footer,
        ]

        page.add(ft.Column(content, spacing=14, tight=True))
        page.update()

    show_login_page()

if __name__ == "__main__":
    ft.app(target=main)