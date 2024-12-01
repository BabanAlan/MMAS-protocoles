import tkinter as tk
from tkinter import filedialog, messagebox

global team_num
team_num = 0

class ScoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Подсчет очков")
        self.file_selected = False  # Флаг, указывающий, был ли выбран файл

        # Главное окно с кнопкой выбора файла
        self.start_frame = tk.Frame(self.root, padx=50, pady=50)
        self.start_frame.pack()
        self.division = ""

        tk.Label(self.start_frame, text="Выберите файл с участниками", font=("Arial", 18)).pack(pady=20)
        tk.Button(self.start_frame, text="Выбрать файл", font=("Arial", 18), command=self.load_participants).pack(pady=10)


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
        # Удаляем все виджеты, включая кнопку
        for widget in self.root.winfo_children():
            widget.destroy()

        self.file_selected = True
        self.root.title(self.division)
        global team_num
        team_num = 0  # Сбрасываем номер команды для правильного расположения

        # Создаем фреймы для команд
        self.blue_frame = self.create_team_frame("Синие", self.blue_scores, "#0D99FF", "#ADD8E6", "#A6C7DF")
        self.red_frame = self.create_team_frame("Красные", self.red_scores, "#F24822", "#FFC7C2", "#DFAEAA")

        # Фрейм для кнопки "Выбрать файл"
        button_frame = tk.Frame(self.root, borderwidth=2)
        button_frame.grid(column=0, row=1, columnspan=2, sticky="ew", pady=15)  # Располагаем под командами
        
        tk.Button(button_frame, text="Результаты", font=("Arial", 18), command=self.show_results).pack(side="top")
        tk.Button(button_frame, text="Новый Дивизион", font=("Arial", 18), command=self.load_participants).pack(side="left", padx=(30, 0), pady=(30, 0))



    def create_team_frame(self, team_name, scores, color, label_bg, border_color):
        global team_num
        frame = tk.Frame(self.root, bg=color, bd=3, relief="solid", padx=30, pady=30)  # Внутренние отступы
        # frame.pack(side=tk.LEFT, padx=30, pady=15)
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

        return frame


    def create_player_row(self, parent, player, scores, index, label_bg, border_color):
        # Основная строка с границей
        row = tk.Frame(parent, bg="white", relief="solid", bd=0, highlightbackground=border_color, highlightthickness=1)
        row.grid(row=index, column=0, sticky="nsew", padx=0, pady=0)

        # Левая часть строки — с цветным фоном и увеличенными отступами
        tk.Label(
            row,
            text=player,
            bg=label_bg,
            fg="black",
            width=25,  # Увеличиваем ширину метки
            anchor="w",
            font=("Arial", 16),  # Уменьшаем шрифт для длинных имен
            padx=20,
            pady=10,
            wraplength=300  # Включаем перенос текста, максимальная ширина — 300px
        ).pack(side=tk.LEFT, fill="both")

        # Кнопка "-"
        minus_button = tk.Button(row, text="-", font=("Arial", 18), width=5, height=2, command=lambda p=player: self.update_score(scores, p, -1), bd=0, relief="flat")
        minus_button.pack(side=tk.LEFT)

        # Метка с текущим счетом
        score_label = tk.Label(row, text="0", bg="white", fg="black", width=6, font=("Arial", 18))
        score_label.pack(side=tk.LEFT)
        scores[player] = score_label

        # Кнопка "+"
        plus_button = tk.Button(row, text="+", font=("Arial", 18), width=5, height=2, command=lambda p=player: self.update_score(scores, p, 1), bd=0, relief="flat")
        plus_button.pack(side=tk.LEFT)


    def update_score(self, scores, player, delta):
        current_score = int(scores[player]["text"])
        new_score = current_score + delta  # Теперь счет может быть и отрицательным
        scores[player]["text"] = str(new_score)
        self.update_total_score(scores)


    def update_total_score(self, scores):
        total = sum(int(label["text"]) for player, label in scores.items() if player not in ["total_label", "players_frame"])
        scores["total_label"]["text"] = f"Счёт: {total}"

    def show_results(self):
        """
        Показывает результаты в новом окне.
        Отображает две отдельные таблицы с игроками каждой команды, отсортированными по количеству очков.
        """
        # Создаем новое окно
        results_window = tk.Toplevel(self.root)
        results_window.title(f"Результаты {self.division}")
        results_window.geometry("950x600")
        results_window.configure(padx=20, pady=20)

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

        # Фрейм для таблиц
        tables_frame = tk.Frame(results_window)
        tables_frame.pack(pady=20)

        # Создаем таблицы для каждой команды
        for team_name, team_scores, team_color in [("Синие", self.blue_scores, "#ADD8E6"), ("Красные", self.red_scores, "#FFC7C2")]:
            # Сортируем игроков команды по количеству очков (по убыванию)
            sorted_team = sorted(
                [(player, int(label["text"])) for player, label in team_scores.items() if player not in ["total_label", "players_frame"]],
                key=lambda x: x[1],
                reverse=True
            )

            # Фрейм для команды
            team_frame = tk.Frame(tables_frame, bg=team_color, padx=15, pady=15, bd=2, relief="solid")
            team_frame.pack(side="left", padx=10)

            # Заголовок таблицы
            tk.Label(
                team_frame,
                text=f"Команда {team_name}",
                font=("Arial", 16, "bold"),
                bg=team_color,
                fg="black"
            ).grid(row=0, column=0, columnspan=2, pady=10)

            # Заголовки столбцов
            tk.Label(team_frame, text="Игрок", font=("Arial", 14, "bold"), bg=team_color, anchor="w", width=20).grid(row=1, column=0, padx=5, pady=5)
            tk.Label(team_frame, text="Очки", font=("Arial", 14, "bold"), bg=team_color, width=10).grid(row=1, column=1, padx=5, pady=5)

            # Заполняем таблицу для команды
            for row_index, (player, score) in enumerate(sorted_team, start=2):
                tk.Label(
                    team_frame,
                    text=player,
                    font=("Arial", 12),
                    bg="white",
                    anchor="w",
                    width=20
                ).grid(row=row_index, column=0, padx=5, pady=2)
                tk.Label(
                    team_frame,
                    text=str(score),
                    font=("Arial", 12),
                    bg="white",
                    width=10
                ).grid(row=row_index, column=1, padx=5, pady=2)

        # Кнопка закрытия окна
        tk.Button(
            results_window,
            text="Закрыть",
            font=("Arial", 14),
            command=results_window.destroy
        ).pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = ScoreApp(root)
    root.mainloop()
