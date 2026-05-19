import flet as ft
import database
import auth
import operations
import export_operations
import analysis
import time
import lang
 
def main(page: ft.Page):
    page.title="Vault100 - Secure Financial Engine"
    page.theme_mode=ft.ThemeMode.DARK
    page.bgcolor="#111111"
    page.window.width=700
    page.window.height=900
    page.padding=0
 
    database.initialize_database()
 
    state={"lang":"English"} #ilk başlatmada türkçeye alınca bozuluyor
 
    def t(key):
        return lang.get(state["lang"],key)
 
    #all of the purpose of this func is to clear the page b4 some functions so they work properly
    def clear_page():
        page.controls.clear()
        page.scroll=None
        page.padding=0
 
    def language_selector(change_fn):
        btns=[]
        for name in lang.LANGUAGES.keys():
            is_active=name==state["lang"]
            def make_click(ln):
                def click(e):
                    change_fn(ln)
                return click
            btns.append(
                ft.TextButton(
                    name,
                    on_click=make_click(name),
                    style=ft.ButtonStyle(
                        color=ft.Colors.BLUE if is_active else ft.Colors.GREY_400,
                    )
                )
            )
        return ft.Row(btns,spacing=2)
    
    def centered_page(card_widget):
        return ft.Row(
            [
                ft.Column(
                    [card_widget],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    #signup page
    """idk when but i should add this one time (19.04)
    that thing doesnt work (28.04) but it will
    shout out to claude for making everything a button. i couldnt get dropdown to work.
    finally finished"""
    #pointer 1
    def show_signup_page():
        clear_page()
 
        uname=ft.TextField(label=t("choose_username"),prefix_icon=ft.Icons.PERSON, width=280)
        pwd=ft.TextField(
            label=t("choose_password"),prefix_icon=ft.Icons.LOCK,
            password=True,can_reveal_password=True, width=280
        )
        pwd2 = ft.TextField(
            label=t("confirm_password"),prefix_icon=ft.Icons.LOCK,
            password=True,can_reveal_password=True, width=280
        )
        msg = ft.Text("",size=13)
 
        def lang_changed(lang_name):
            state["lang"]=lang_name
            page.title=t("app_title")
            show_signup_page()
 
        def signup_handler(e):
            if pwd.value!=pwd2.value:
                msg.value=t("passwords_no_match")
                msg.color=ft.Colors.RED
                page.update()
                return
            success,message=auth.register_user(uname.value, pwd.value)
            msg_map={
                "Username and password cannot be empty.":t("add_required"),
                "Username must be at least 3 characters.":t("username_min"),
                "Password must be at least 4 characters.":t("password_min"),
                "Username already taken.":t("username_taken"),
                "Account created! Redirecting to login...":t("register_success"), # doesnt redirect. // fixed
                "Registration failed. Try again.":t("register_fail"),
            }
            msg.value=msg_map.get(message,message)
            msg.color=ft.Colors.GREEN if success else ft.Colors.RED
            page.update()
            if success:
                def go_login():
                    time.sleep(1.5)
                    show_login_page()
                page.run_thread(go_login)
 
        card = ft.Container(
            width=420,
            padding=40,
            bgcolor="#1E1E1E",
            border_radius=12,
            border=ft.border.all(1, "#333333"),
            content=ft.Column(
                [
                    ft.Row([
                        ft.Text(t("language"),size=13,color=ft.Colors.GREY),
                        language_selector(lang_changed),
                    ], alignment=ft.MainAxisAlignment.END),
                    ft.Icon(ft.Icons.PERSON_ADD,size=50,color=ft.Colors.BLUE),
                    ft.Text(t("signup_title"),size=26,weight=ft.FontWeight.BOLD),
                    ft.Text(t("signup_subtitle"),size=13,color=ft.Colors.GREY),
                    ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
                    uname,
                    pwd,
                    pwd2,
                    msg,
                    ft.ElevatedButton(t("create_account"),width=280,on_click=signup_handler),
                    ft.TextButton(t("have_account"),on_click=lambda _:show_login_page()),#hesabın varsa girişe dönmeli // fixed
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=14,
                tight=True,
            ),
        )
 
        page.add(centered_page(card))
        page.update()
 
    #login page. first thing user sees. also the most important one.
    
    def show_login_page():
        clear_page()
 
        username_field=ft.TextField(label=t("username"),prefix_icon=ft.Icons.PERSON,width=280)
        password_field=ft.TextField(
            label=t("password"),prefix_icon=ft.Icons.LOCK,
            password=True,can_reveal_password=True,width=280
        )
        error_text = ft.Text("",color=ft.Colors.RED,size=13) #error vermiyor. bozuk.
 
        def lang_changed(lang_name): #state değişiyor ama sayfa güncellenmiyor 3rd pointer
            state["lang"]=lang_name
            page.title=t("app_title")
            show_login_page()
 
        def login_handler(e):
            user=auth.verify_user(username_field.value, password_field.value)
            if user:
                show_dashboard(user)
            else:
                error_text.value=t("invalid_credentials")
                page.update()
 
        card = ft.Container(
            width=400,
            padding=40,
            bgcolor="#1E1E1E",
            border_radius=12,
            border=ft.border.all(1, "#333333"),
            content=ft.Column(
                [
                    ft.Row([
                        ft.Text(t("language"),size=13,color=ft.Colors.GREY),
                        language_selector(lang_changed),
                    ], alignment=ft.MainAxisAlignment.END),
                    ft.Icon(ft.Icons.SHIELD,size=50,color=ft.Colors.BLUE),
                    ft.Text(t("login_title"),size=28,weight=ft.FontWeight.BOLD),
                    ft.Text(t("login_subtitle"),size=13,color=ft.Colors.GREY),
                    ft.Divider(height=8,color=ft.Colors.TRANSPARENT),
                    username_field,
                    password_field,
                    error_text,
                    ft.ElevatedButton(t("enter_vault"),width=280,on_click=login_handler),
                    ft.TextButton(t("no_account"),on_click=lambda _: show_signup_page()),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=14,
                tight=True,
            ),
        )
 
        page.add(centered_page(card))
        page.update()
 
    
    def show_dashboard(session):
        clear_page() #dashboardda her şeyden önce temizleme yapmazsak bozuluyor ama login ve signupda yapmazsak geri gidince yazdıklarımız kalıyor. bu yüzden ayrı fonksiyonlarda clear_page çağırıyorum.
        page.scroll=ft.ScrollMode.AUTO
        page.padding=ft.padding.only(left=24, right=24, top=12, bottom=30)
 
        is_admin=session["role"] == "admin"
        current_user=session["username"]
 
        view_state={"user": current_user}
 
        def section_title(text):
            return ft.Text(text,size=18,weight=ft.FontWeight.BOLD)
 
        def styled_card(content):
            return ft.Container(
                content=content,
                padding=16,
                bgcolor="#1E1E1E",
                border_radius=10,
                border=ft.border.all(1,"#333333"),
            )
 
        #lang selector. dashboardda da olsun istedim. pointer 7
        def lang_changed_dashboard(lang_name):
            state["lang"]=lang_name
            page.title=t("app_title")
            show_dashboard(session)
 
        lang_row = ft.Row([
            ft.Text(t("language"),size=13,color=ft.Colors.GREY),
            language_selector(lang_changed_dashboard),
        ], alignment=ft.MainAxisAlignment.END)
 
        admin_user_selector=[]
        if is_admin:
            all_users=auth.get_all_users()
 
            user_btns=[]
            for u in all_users:
                is_selected=u["username"]==view_state["user"]
                def make_click(uname):
                    def click(e):
                        view_state["user"]=uname
                        refresh_user_view()
                    return click
                user_btns.append(
                    ft.ElevatedButton(
                        u["username"],
                        on_click=make_click(u["username"]),
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE if is_selected else ft.Colors.GREY_400,
                            bgcolor=ft.Colors.BLUE if is_selected else ft.Colors.TRANSPARENT,
                        ),
                    )
                )
            admin_user_selector=[
                styled_card(ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.MANAGE_ACCOUNTS, color=ft.Colors.BLUE),
                        ft.Text("Kullanıcı Görünümü:", size=13, color=ft.Colors.GREY),
                    ], spacing=8),
                    ft.Row(user_btns, spacing=8, wrap=True),
                ], spacing=8, tight=True)),
            ]
 
        content_col=ft.Column([],spacing=14, tight=True) 
 
        def refresh_user_view():
            viewed_user=view_state["user"]
 
            # bakiye burada. ortalamak istiyorum ama bozuluyor. 
            balance=operations.calculate_current_balance(username=viewed_user)
            balance_card=styled_card(
                ft.Column([
                    ft.Text(
                        t("total_balance")+" — {}".format(viewed_user),
                        size=13, color=ft.Colors.GREY
                    ),
                    ft.Text(
                        "{:.2f} TL".format(balance),
                        size=34, weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREEN if balance >=0 else ft.Colors.RED,
                    ),
                ], spacing=4,tight=True)
            )
 
            #transaction pointer 4 dd // fixed(punctuation)
            amt_input = ft.TextField(
                label=t("amount"),width=130,
                keyboard_type=ft.KeyboardType.NUMBER,
            )
            type_dropdown = ft.Dropdown(
                label=t("type"),width=130,
                options=[
                    ft.dropdown.Option(t("income")),
                    ft.dropdown.Option(t("expense")),
                ],
            )
            #dropdownun çalıştığı tek yer 
            cat_dropdown = ft.Dropdown(
                label=t("category"), width=150,
                options=[
                    ft.dropdown.Option(t("food")),
                    ft.dropdown.Option(t("rent")),
                    ft.dropdown.Option(t("salary")),
                    ft.dropdown.Option(t("bills")),
                    ft.dropdown.Option(t("fun")),
                    ft.dropdown.Option(t("general")),
                ],
            )  
            """ def test_dropdown_changed(e): #dropdown test
                    if cat_dropdown.value==t("food"):
                        page.launch_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                        page.update()
                cat_dropdown.on_change=test_dropdown_changed"""

            desc_input = ft.TextField(label=t("description"),   width=160)
            add_msg = ft.Text("", size=12)
 
            def add_btn_click(e):
                add_msg.value = ""
                if not amt_input.value or not type_dropdown.value:
                    add_msg.value= t("add_required")
                    add_msg.color= ft.Colors.RED
                    page.update()
                    return
                try:
                    float(amt_input.value)
                except ValueError:
                    add_msg.value= t("add_number")
                    add_msg.color= ft.Colors.RED
                    page.update()
                    return
 
                type_en="Income" if type_dropdown.value == t("income") else "Expense"
                cat_map={
                    t("food"): "Food", t("rent"): "Rent", t("salary"): "Salary",
                    t("bills"): "Bills", t("fun"): "Fun", t("general"): "General",
                }
                cat_en=cat_map.get(cat_dropdown.value, cat_dropdown.value or "General")
 
                operations.add_transaction(
                    amt_input.value, cat_en, type_en,
                    desc_input.value or "Manual Entry",
                    viewed_user,
                )
                refresh_user_view()
 
            add_section=styled_card(
                ft.Column([
                    ft.Row(
                        [
                            amt_input, type_dropdown, cat_dropdown, desc_input,
                            ft.IconButton(
                                icon=ft.Icons.ADD_CIRCLE,
                                icon_color=ft.Colors.BLUE,
                                icon_size=36,
                                tooltip=t("quick_add"),
                                on_click=add_btn_click,
                            )
                        ],
                        wrap=True, spacing=8,
                    ),
                    add_msg,
                ], spacing=6, tight=True)
            )
 
            #transaction history. güzel değil çok hantal bir yoldan çalışıyor.
            #pointer 5
            history_data=operations.get_transaction_history(username=viewed_user)
 
            type_display={"Income": t("income"), "Expense": t("expense")}
            cat_display={
                "Food": t("food"), "Rent": t("rent"), "Salary": t("salary"),
                "Bills": t("bills"), "Fun": t("fun"), "General": t("general"),
            }

            #transaction silme // fixed
            def delete_tx_handler(e):
                operations.delete_transaction(e.control.data)
                refresh_user_view()
 
            tx_rows = []
            for i in history_data:
                tx_rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(i["date"], size=12)),
                    ft.DataCell(ft.Text(
                        type_display.get(i["type"], i["type"]), size=12,
                        color=ft.Colors.GREEN if i["type"] == "Income" else ft.Colors.RED,
                    )),
                    ft.DataCell(ft.Text("{:.2f} TL".format(i["amount"]), size=12)),
                    ft.DataCell(ft.Text(cat_display.get(i["category"], i["category"] or "-"), size=12)),
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
                    ft.DataCell(ft.Text(t("no_tx"), color=ft.Colors.GREY)),
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
                            ft.DataColumn(ft.Text(t("date"))),
                            ft.DataColumn(ft.Text(t("type"))),
                            ft.DataColumn(ft.Text(t("amount"))),
                            ft.DataColumn(ft.Text(t("category"))),
                            ft.DataColumn(ft.Text(t("description"))),
                            ft.DataColumn(ft.Text(t("del") if is_admin else "")),
                        ],
                        rows=tx_rows,
                        horizontal_margin=8,
                        column_spacing=12,
                    )
                ], scroll=ft.ScrollMode.AUTO)
            )
            #where to use analyse 
            totals=analysis.get_income_vs_expense(username=viewed_user)
            cat_totals=analysis.get_category_totals(username=viewed_user)
            net = totals["Income"] - totals["Expense"]
 
            def mini_card(label, value, color):
                return ft.Container(
                    content=ft.Column([
                        ft.Text(label, color=ft.Colors.GREY, size=12),
                        ft.Text(
                            "{:.2f} TL".format(value),
                            color=color, size=20, weight=ft.FontWeight.BOLD
                        ),
                    ], tight=True, spacing=4),
                    padding=16, bgcolor="#1E1E1E",
                    border_radius=8, border=ft.border.all(1, "#333333"),
                    expand=True,
                )
 
            cat_rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(cat_display.get(cat, cat))),
                    ft.DataCell(ft.Text("{:.2f} TL".format(amt), color=ft.Colors.RED)),
                ]) for cat, amt in sorted(cat_totals.items(), key=lambda x: x[1], reverse=True)
            ] or [ft.DataRow(cells=[
                ft.DataCell(ft.Text(t("no_expense_data"), color=ft.Colors.GREY)),
                ft.DataCell(ft.Text("")),
            ])]
 
            analysis_section = styled_card(ft.Column([
                ft.Row([
                    mini_card(t("total_income"), totals["Income"], ft.Colors.GREEN),
                    mini_card(t("total_expense"), totals["Expense"], ft.Colors.RED),
                    mini_card(t("net"), net, ft.Colors.GREEN if net >= 0 else ft.Colors.RED),
                ], spacing=10),
                ft.Text(t("expense_by_cat"), size=14, color=ft.Colors.GREY),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text(t("category"))),
                        ft.DataColumn(ft.Text(t("total_spent"))),
                    ],
                    rows=cat_rows,
                    horizontal_margin=8,
                    column_spacing=16,
                ),
            ], spacing=10, tight=True))
 
            #export
            start_field = ft.TextField(
                label=t("from_date"), width=180, hint_text=t("optional")
            )
            end_field = ft.TextField(
                label=t("to_date"), width=180, hint_text=t("optional")
            )
            export_msg = ft.Text("", size=12)
 
            def export_handler(e):
                path = export_operations.export_to_text(
                    username=viewed_user,
                    start_date=start_field.value or None,
                    end_date=end_field.value or None,
                )
                if path:
                    export_msg.value = t("export_saved") + path
                    export_msg.color = ft.Colors.GREEN
                else:
                    export_msg.value = t("export_fail")
                    export_msg.color = ft.Colors.RED
                page.update()
 
            export_section = styled_card(ft.Column([
                ft.Row([
                    start_field, end_field,
                    ft.ElevatedButton(
                        t("export_btn"), icon=ft.Icons.FILE_DOWNLOAD, on_click=export_handler
                    ),
                ], spacing=10, wrap=True),
                export_msg,
            ], spacing=6, tight=True))
 
            # admin kontrolleri pointer 2
            #admin her userda aynı bakiyeyi görüyor. tek tek görmek istediği userı seçmesi lazım
            """admin kontrollerini ayrı bir kısım olarak yapmayı planlamıştım 
            ama dropdown çalışmayınca her yere buton koydum
            ve yine çalışmadı"""
            # fixed with ai. couldn't compete with claude on this one.
            admin_controls=[]
            if is_admin:
                all_users_list = auth.get_all_users()
 
                new_uname=ft.TextField(label=t("username"), width=140)
                new_pass=ft.TextField(label=t("password"), width=140, password=True)
                new_role=ft.Dropdown(
                    label=t("role"), width=120,
                    options=[ft.dropdown.Option("user"),ft.dropdown.Option("admin")],
                )
                add_user_msg = ft.Text("",size=12)
 
                def add_user_handler(e):
                    if not new_uname.value or not new_pass.value or not new_role.value:
                        add_user_msg.value = t("all_fields")
                        add_user_msg.color = ft.Colors.RED
                        page.update()
                        return
                    success = auth.add_user(new_uname.value, new_pass.value, new_role.value)
                    if success:
                        show_dashboard(session)
                    else:
                        add_user_msg.value = t("user_exists")
                        add_user_msg.color = ft.Colors.RED
                        page.update()

                #kullanıcı silme
                def del_user_handler(e): 
                    auth.delete_user(e.control.data)
                    show_dashboard(session)
 
                user_rows=[
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
                    ])for u in all_users_list
                ]
 
                admin_controls=[
                    ft.Divider(height=1,thickness=1),
                    section_title(t("admin_title")),
                    styled_card(ft.Column([
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text(t("username"))),
                                ft.DataColumn(ft.Text(t("role"))),
                                ft.DataColumn(ft.Text(t("remove"))),
                            ],
                            rows=user_rows,
                            horizontal_margin=8,
                            column_spacing=16,
                        ),
                        ft.Divider(height=1),
                        ft.Text(t("add_user_title"), size=13, color=ft.Colors.GREY),
                        ft.Row([
                            new_uname, new_pass, new_role,
                            ft.ElevatedButton(t("add_btn"), on_click=add_user_handler),
                        ], spacing=8, wrap=True),
                        add_user_msg,
                    ], spacing=10, tight=True)),
                ]
 
            # footer 
            footer = ft.Row([
                ft.Row([
                    ft.Icon(ft.Icons.PERSON, size=15, color=ft.Colors.GREY),
                    ft.Text(
                        "{} ({})".format(session["username"], session["role"]),
                        color=ft.Colors.GREY,size=12,
                    ),
                ], spacing=4),
                ft.TextButton(t("logout"),on_click=lambda _:show_login_page()),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
 
            content_col.controls = [
                ft.Row([
                    ft.Text(t("dashboard_title"), size=26, weight=ft.FontWeight.BOLD),
                    lang_row,
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                *admin_user_selector,
                balance_card,
                ft.Divider(height=1, thickness=1),
                section_title(t("quick_add")),
                add_section,
                ft.Divider(height=1, thickness=1),
                section_title(t("tx_history")),
                history_table,
                ft.Divider(height=1, thickness=1),
                section_title(t("analysis")),
                analysis_section,
                ft.Divider(height=1, thickness=1),
                section_title(t("export_title")),
                export_section,
                *admin_controls,
                ft.Divider(height=1, thickness=1),
                footer,
            ]
            page.update()
        page.add(content_col)
        refresh_user_view()

    show_login_page()
 
 # flet şunu yazmadan başlamıyor
if __name__ == "__main__":
    ft.app(target=main)