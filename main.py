import tkinter as tk
from tkinter import filedialog, messagebox, ttk

global team_num
team_num = 0

class ScoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Подсчет очков")
        self.file_selected = False  # Флаг, указывающий, был ли выбран файл
        
        self.active_blue_player = None
        self.active_red_player = None

        # Главное окно с кнопкой выбора файла
        self.start_frame = tk.Frame(self.root, padx=50, pady=50)
        self.start_frame.pack()
        self.division = ""

        tk.Label(self.start_frame, text="Выберите файл с участниками", font=("Arial", 18)).pack(pady=20)
        tk.Button(self.start_frame, text="Выбрать файл", font=("Arial", 18), cursor="hand2", command=self.load_participants).pack(pady=10)


    def load_participants(self):
        """
        Загружает участников из выбранного текстового файла.
        Участники формируются на основе заголовков:
        "Команда синих:" и "Команда красных:".
        """

        file_path = filedialog.askopenfilename(
            title="Выберите файл с участниками",
            filetypes=(("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")),
        )
        self.division = file_path.split('/')[-1][:-4]

        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                lines = [line.strip() for line in file if line.strip()]
                
                # Разделяем участников по заголовкам
                blue_start = lines.index("Команда синих:") + 1
                red_start = lines.index("Команда красных:") + 1

                blue_team = lines[blue_start:lines.index("Команда красных:")]
                red_team = lines[red_start:]

                if not blue_team or not red_team:
                    raise ValueError("Не найдены участники для одной из команд.")

                self.blue_scores = {name: 0 for name in blue_team}
                self.red_scores = {name: 0 for name in red_team}

                self.blue_missed = {name: 0 for name in self.blue_scores}  # Пропущенные очки для синих
                self.red_missed = {name: 0 for name in self.red_scores}  # Пропущенные очки для красных

                    # Удаляем все виджеты, включая кнопку
            for widget in self.root.winfo_children():
                widget.pack_forget()
            # После успешного выбора файла отображаем команды

            self.display_teams()

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить участников: {e}")


    def display_teams(self):
        """
        Отображает команды на экране после выбора файла.
        """

        self.file_selected = True
        self.root.title(self.division)

        global team_num
        team_num = 0  # Сбрасываем номер команды для правильного расположения

        try:
            self.blue_frame.grid_forget()
            self.red_frame.grid_forget()
        except:
            pass

        # Создаем фреймы для команд
        self.blue_frame = self.create_team_frame("Синие", self.blue_scores, "#0D92FF", "#ADD8E6", "#A6C7DF", "blue")
        self.red_frame = self.create_team_frame("Красные", self.red_scores, "#FF390D", "#FFC7C2", "#DFAEAA", "red")

        # Фрейм для кнопки "Выбрать файл"
        button_frame = tk.Frame(self.root, borderwidth=2)
        button_frame.grid(column=0, row=1, columnspan=2, sticky="ew", pady=15)  # Располагаем под командами
        
        tk.Button(button_frame, text="Результаты", font=("Arial", 18), cursor="hand2", command=self.show_results).pack(side="top")
        tk.Button(button_frame, text="Новый Дивизион", font=("Arial", 18 ), cursor="hand2", command=self.load_participants).pack(side="left", padx=(30, 0), pady=(30, 0))


    def create_team_frame(self, team_name, scores, color, label_bg, border_color, team):
        global team_num
        frame = tk.Frame(self.root, bg=color, bd=3, relief="solid", padx=30, pady=30)  # Внутренние отступы
        frame.grid(column=team_num, row=0, padx=30, pady=15)
        team_num += 1
        # Заголовок команды
        tk.Label(frame, text=team_name, bg=color, font=("Arial", 24, "bold"), fg="white").pack()

        # Список игроков
        players_frame = tk.Frame(frame, bg="white")
        players_frame.pack(pady=15)
        scores["players_frame"] = players_frame

        # Создаем строки игроков
        for index, player in enumerate(scores):
            if player != "players_frame" and player != "total_label":
                self.create_player_row(players_frame, player, scores, index, label_bg, border_color)

        # Общий счет
        total_label = tk.Label(frame, text="Счёт: 0", bg=color, fg="white", font=("Arial", 20), pady=10)
        total_label.pack(pady=15)
        scores["total_label"] = total_label

        # Кнопки для изменения общего счета команды и счета активного игрока
        button_frame = tk.Frame(frame, bg=color)
        button_frame.pack(pady=10)

        # Кнопка "-" для уменьшения счета
        minus_button = tk.Button(button_frame, text="-", width=10, font=("Arial", 30), cursor="hand2", command=lambda: self.update_team_score(scores, -1, team))
        minus_button.pack(side="left", padx=10)

        # Кнопка "+" для увеличения счета
        plus_button = tk.Button(button_frame, text="+", width=10, font=("Arial", 30), cursor="hand2", command=lambda: self.update_team_score(scores, 1, team))
        plus_button.pack(side="left", padx=10)

        return frame


    def update_team_score(self, scores, delta, team):
        if self.active_blue_player and self.active_red_player:
            # Обновляем общий счет команды
            total_score = int(scores["total_label"]["text"].split(":")[1].strip())
            new_total_score = total_score + delta
            scores["total_label"]["text"] = f"Счёт: {new_total_score}"

            # Обновляем счет активного игрока в данной команде
            if team == "blue" and self.active_blue_player:
                active_player = self.active_blue_player[0]
                self.update_player_score(self.blue_scores, active_player, delta)
                # Увеличиваем пропущенные очки для активного игрока красной команды
                if self.active_red_player:
                    self.red_missed[self.active_red_player[0]] += abs(delta)

            elif team == "red" and self.active_red_player:
                active_player = self.active_red_player[0]
                self.update_player_score(self.red_scores, active_player, delta)
                # Увеличиваем пропущенные очки для активного игрока синей команды
                if self.active_blue_player:
                    self.blue_missed[self.active_blue_player[0]] += abs(delta)


    def update_player_score(self, scores, player, delta):
        # Обновляем счет конкретного игрока
        current_score = int(scores[player]["text"])
        new_score = current_score + delta
        scores[player]["text"] = str(new_score)
        self.update_total_score(scores)


    def create_player_row(self, parent, player, scores, index, label_bg, border_color):
        """
        Создает строку игрока с чекбоксом, именем, счетом и кнопками.
        Чекбокс расположен слева от имени игрока.
        """
        # Основная строка с границей
        row = tk.Frame(parent, bg="white", relief="solid", bd=0, highlightbackground=border_color, highlightthickness=1)
        row.grid(row=index, column=0, sticky="nsew", padx=0, pady=0)

        # Функции изменения цвета фона при наведении
        def on_hover(event):
            if player in self.blue_scores and (not self.active_blue_player or self.active_blue_player[0] != player):
                name_label.config(bg="#87CEEB")  # Более яркий цвет для синей команды
            elif player in self.red_scores and (not self.active_red_player or self.active_red_player[0] != player):
                name_label.config(bg="#FF958C")  # Более яркий цвет для красной команды
            self.root.config(cursor="hand2")

        def on_leave(event):
            if player in self.blue_scores and (not self.active_blue_player or self.active_blue_player[0] != player):
                name_label.config(bg=label_bg)  # Возвращаем исходный цвет
            elif player in self.red_scores and (not self.active_red_player or self.active_red_player[0] != player):
                name_label.config(bg=label_bg)  # Возвращаем исходный цвет
            self.root.config(cursor="arrow")


        # Обработчик клика на метку имени игрока
        def on_click(event):
            if var.get() == 0:  # Если чекбокс не активен
                var.set(1)  # Активируем чекбокс
                self.set_active_player(var, player, scores, name_label)  # Устанавливаем активного игрока

        # Галочка для активации игрока
        var = tk.IntVar()
        check_button = tk.Checkbutton(
            row,
            variable=var,
            font=("Arial", 18),
            command=lambda: self.set_active_player(var, player, scores, name_label),
            width=0
        )
        check_button.pack_forget()

        # Левая часть строки — метка с именем игрока
        name_label = tk.Label(
            row,
            text=player,
            bg=label_bg,
            fg="black",
            width=31,
            anchor="w",
            font=("Arial", 16),
            padx=20,
            pady=10,
            wraplength=300
        )
        name_label.pack(side=tk.LEFT, fill="both")
        name_label.bind("<Enter>", on_hover)  # Наведение курсора
        name_label.bind("<Leave>", on_leave)  # Уход курсора
        name_label.bind("<Button-1>", on_click)  # Клик по области имени

        # Метка счета игрока
        score_label = tk.Label(row, text="0", bg="white", fg="black", width=6, font=("Arial", 18))
        score_label.pack(side=tk.LEFT)
        scores[player] = score_label


    def set_active_player(self, var, player, scores, name_label):
        """
        Устанавливает активного игрока для команды.
        Меняет фон метки имени активного игрока на яркий цвет, а у предыдущего активного игрока возвращает исходный цвет.
        """
        if player in self.blue_scores:  # Если игрок принадлежит синей команде
            if var.get() == 1:  # Если галочка установлена
                # Сбрасываем предыдущего активного игрока
                if self.active_blue_player:
                    self.active_blue_player[1].set(0)  # Снимаем галочку
                    self.active_blue_player[2].config(bg="#ADD8E6")  # Возвращаем исходный цвет имени

                # Устанавливаем нового активного игрока
                self.active_blue_player = (player, var, name_label)
                name_label.config(bg="#6DB3E5")  # Устанавливаем яркий цвет для имени

        elif player in self.red_scores:  # Если игрок принадлежит красной команде
            if var.get() == 1:  # Если галочка установлена
                # Сбрасываем предыдущего активного игрока
                if self.active_red_player:
                    self.active_red_player[1].set(0)  # Снимаем галочку
                    self.active_red_player[2].config(bg="#FFC7C2")  # Возвращаем исходный цвет имени

                # Устанавливаем нового активного игрока
                self.active_red_player = (player, var, name_label)
                name_label.config(bg="#CF4E4E")  # Устанавливаем яркий цвет для имени


    def update_score(self, scores, team, delta):
        # Проверяем, какой команде нужно обновить счет
        if team == "blue" and self.active_blue_player:
            player = self.active_blue_player[0]
            current_score = int(scores[player]["text"])
            new_score = current_score + delta
            scores[player]["text"] = str(new_score)
            self.update_total_score(scores)

        elif team == "red" and self.active_red_player:
            player = self.active_red_player[0]
            current_score = int(scores[player]["text"])
            new_score = current_score + delta
            scores[player]["text"] = str(new_score)
            self.update_total_score(scores)


    def update_total_score(self, scores):
        total = sum(int(label["text"]) for player, label in scores.items() if player not in ["total_label", "players_frame"])
        scores["total_label"]["text"] = f"Счёт: {total}"


    def show_results(self):
        """
        Показывает результаты в новом окне.
        Отображает одну общую таблицу с игроками обеих команд, с фильтрацией по кнопкам.
        """
        # Создаем новое окно
        results_window = tk.Toplevel(self.root)
        results_window.title(f"Результаты {self.division}")
        results_window.geometry("800x600")
        results_window.configure(padx=20, pady=20)

        active_column = None

        # Вычисляем общий счет каждой команды
        blue_total = sum(int(label["text"]) for player, label in self.blue_scores.items() if player not in ["total_label", "players_frame"])
        red_total = sum(int(label["text"]) for player, label in self.red_scores.items() if player not in ["total_label", "players_frame"])

        # Определяем победителя
        if blue_total > red_total:
            winner_text = "Победила команда Синих!"
            winner_color = "#0D99FF"
        elif red_total > blue_total:
            winner_text = "Победила команда Красных!"
            winner_color = "#F24822"
        else:
            winner_text = "Ничья!"
            winner_color = "gray"

        # Заголовок с результатом
        tk.Label(
            results_window,
            text=winner_text,
            font=("Arial", 18, "bold"),
            fg=winner_color
        ).pack(pady=10)

        # Общий счет команд
        tk.Label(
            results_window,
            text=f"Общий счет: {blue_total} : {red_total}",
            font=("Arial", 18, "bold"),
            justify="left"
        ).pack(pady=10)

        # Подготовка данных для общей таблицы
        combined_scores = []
        for player, label in self.blue_scores.items():
            if player not in ["total_label", "players_frame"]:
                combined_scores.append((player, int(label["text"]), self.blue_missed[player],
                                        int(label["text"]) - self.blue_missed[player],
                                        round(int(label["text"]) / max(self.blue_missed[player], 1), 2), "Синие"))
        for player, label in self.red_scores.items():
            if player not in ["total_label", "players_frame"]:
                combined_scores.append((player, int(label["text"]), self.red_missed[player],
                                        int(label["text"]) - self.red_missed[player],
                                        round(int(label["text"]) / max(self.red_missed[player], 1), 2), "Красные"))

        # Кнопки для фильтрации
        button_frame = tk.Frame(results_window)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Синие", font=("Arial", 14), command=lambda: update_table("Синие")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Красные", font=("Arial", 14), command=lambda: update_table("Красные")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Все", font=("Arial", 14), command=lambda: update_table("Все")).pack(side=tk.LEFT, padx=5)

        # Изначальная сортировка и состояние
        current_sort_column = [4]  # Индекс столбца для сортировки, по умолчанию КПД
        current_sort_order = [True]  # Порядок сортировки: True - по убыванию, False - по возрастанию

        # Создаем фрейм для таблицы
        table_frame = tk.Frame(results_window)
        table_frame.pack(pady=20)

        # Заголовки столбцов
        headers = ["Игрок ▼", "   Очки ▼   ", "Пропустил ▼", "Разница ▼", "КПД ▼", "Команда ▼"]

        def sort_table_by_column(column_index):
            """Функция для сортировки данных по выбранному столбцу."""
            if current_sort_column[0] == column_index:
                current_sort_order[0] = not current_sort_order[0]  # Меняем порядок сортировки
            else:
                current_sort_column[0] = column_index
                current_sort_order[0] = True  # Сброс на сортировку по убыванию
            combined_scores.sort(key=lambda x: x[column_index], reverse=current_sort_order[0])
            update_table()
            
            
        # Функция для обновления таблицы в зависимости от фильтра
        def update_table(filter_team="Все"):
            # Очистка предыдущих данных в таблице
            for widget in table_frame.winfo_children():
                widget.destroy()

            # Заголовки столбцов
            for col_index, header in enumerate(headers):
                label = tk.Label(
                    table_frame,
                    text=header,
                    font=("Arial", 14, "bold"),
                    bg="#DDDDDD",
                    padx=10,
                    pady=5,
                    borderwidth=1,
                    relief="solid",
                    cursor="hand2"
                )
                label.grid(row=0, column=col_index, sticky="nsew")
                label.bind("<Button-1>", lambda e, col=col_index: sort_table_by_column(col))  # Привязка клика
                label.bind("<Enter>", lambda e: e.widget.config(bg="#B9B9B9"))
                label.bind("<Leave>", lambda e: e.widget.config(bg="#DDDDDD"))

            # Фильтрация и вывод данных
            row_index = 1
            for player, score, missed, diff, effic, team in combined_scores:
                if filter_team == "Все" or team == filter_team:
                    bg_color = "#ADD8E6" if team == "Синие" else "#FFC7C2"
                    data = [player, score, missed, diff, effic, team]
                    for col_index, value in enumerate(data):
                        tk.Label(
                            table_frame,
                            text=str(value),
                            font=("Arial", 12),
                            bg=bg_color,
                            padx=10,
                            pady=5,
                            borderwidth=1,
                            relief="solid"
                        ).grid(row=row_index, column=col_index, sticky="nsew")
                    row_index += 1

        # Изначально отображаем всю таблицу
        combined_scores.sort(key=lambda x: x[current_sort_column[0]], reverse=current_sort_order[0])
        update_table()

        # Кнопка закрытия окна
        tk.Button(
            results_window,
            text="Закрыть",
            font=("Arial", 14),
            cursor="hand2",
            command=results_window.destroy
        ).pack(pady=20)

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = ScoreApp(root)
    root.mainloop()
