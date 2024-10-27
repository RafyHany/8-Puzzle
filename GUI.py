from customtkinter import *
import customtkinter as ctk
from Algorithms.Astar import *
from Algorithms.BFS import *
from Algorithms.dfs import *
from Algorithms.iterativeDFS import *


def create_step_viewer(app, result):
    result_begin = 0
    result_limit = 30  # End limit

    def show_next_batch():
        nonlocal result_limit, result_begin  # Added result_begin here
        if result_limit < len(result[0]):
            show_steps(app, result[0][result_begin:result_limit], result[4], result[2], result[1])
            result_begin = result_limit
            result_limit += 30

        # Disable button if we've shown everything
        if result_limit >= len(result[0]):
            next_button.configure(state="disabled")

    # Create the button
    next_button = ctk.CTkButton(
        master=app,
        width=80,
        height=35,
        corner_radius=25,
        fg_color="#ee4266",
        border_color="#c7ef00",
        hover_color="#a1286a",
        text="Get Next Batch",
        font=("Digital-7 Mono", 20, "bold"),
        command=show_next_batch
    )
    next_button.place(relx=0.4, rely=0.8)

    # Show first batch immediately
    show_next_batch()


def show_steps(app, states, time_taken, nodes_expanded, search_depth):
    steps_frame = ctk.CTkScrollableFrame(app,
                                         fg_color="#540d6e",
                                         corner_radius=0)
    steps_frame.place(relx=0.7, rely=0.35)

    for i in range(len(states)):

        state = states[i][0]

        st = ctk.CTkFrame(steps_frame,
                          fg_color='black',
                          width=80,
                          height=50)

        st.pack(pady=10)

        state_str = str(state).zfill(9)
        formatted_state = [state_str[i:i + 3] for i in range(0, len(state_str), 3)]
        state_string = "\n".join([f"[{' '.join(row)}]" for row in formatted_state])

        ctk.CTkLabel(st,
                     font=("Digital-7 Mono", 28, "bold"),
                     text=state_string).pack()

        if states[i][1] != "":
            direction = ctk.CTkFrame(steps_frame,
                                     fg_color='red',
                                     width=80,
                                     height=50)

            direction.pack(pady=10)

            ctk.CTkLabel(direction,
                         font=("Digital-7 Mono", 28, "bold"),
                         text=f"{i + 1} - {states[i][1]}").pack()

    results = ctk.CTkFrame(app,
                           fg_color="#540d6e")

    results.place(relx=0.7, rely=0.7)

    ctk.CTkLabel(results,
                 font=("Digital-7 Mono", 18, "bold"),
                 text=f"Time Taken:{time_taken:.5f}").pack(pady=10)

    ctk.CTkLabel(results,
                 font=("Digital-7 Mono", 18, "bold"),
                 text=f"Nodes Expanded:{nodes_expanded}").pack(pady=10)

    ctk.CTkLabel(results,
                 font=("Digital-7 Mono", 18, "bold"),
                 text=f"search depth:{search_depth}").pack(pady=10)


def show_optional_choices(s, app):
    if s == "A*":
        manhattan_var = ctk.StringVar(value="off")
        euclidean_var = ctk.StringVar(value="off")
        app.selected_heuristic = ctk.StringVar(value="")

        def manhattan_clicked():
            if manhattan_var.get() == "on":
                euclidean_var.set("off")
                app.selected_heuristic.set("manhattan")
                # print("Selected heuristic:", app.selected_heuristic.get())
            else:
                app.selected_heuristic.set("")
            h2.deselect()

        def euclidean_clicked():
            if euclidean_var.get() == "on":
                manhattan_var.set("off")
                app.selected_heuristic.set("euclidean")
                # print("Selected heuristic:", app.selected_heuristic.get())
            else:
                app.selected_heuristic.set("")
            h1.deselect()

        h1 = ctk.CTkCheckBox(master=app,
                             text="Manhattan",
                             width=80,
                             variable=manhattan_var,
                             onvalue="on",
                             offvalue="off",
                             command=manhattan_clicked)
        h1.place(relx=0.45, rely=0.8, anchor="center")

        h2 = ctk.CTkCheckBox(master=app,
                             text="Euclidean",
                             width=80,
                             variable=euclidean_var,
                             onvalue="on",
                             offvalue="off",
                             command=euclidean_clicked)
        h2.place(relx=0.6, rely=0.8, anchor="center")

        app.manhattan_var = manhattan_var
        app.euclidean_var = euclidean_var
    else:
        ctk.CTkFrame(master=app,
                     height=50,
                     width=800,
                     fg_color="#540d6e").place(relx=0.5225, rely=0.3, anchor="center")

        ctk.CTkFrame(master=app,
                     height=100,
                     width=800,
                     fg_color="#540d6e").place(relx=0.5225, rely=0.8, anchor="center")


def show_board(app, frame_side_length, padding, state_str=None):
    entries = []

    for col in range(3):
        for row in range(3):
            frame = CTkFrame(master=app,
                             width=frame_side_length,
                             height=frame_side_length,
                             corner_radius=0,
                             fg_color="#f78a53")
            frame.place(relx=0.395 + row * (padding / 800), rely=0.375 + col * (padding / 600))

    for col in range(3):
        for row in range(3):
            frame = CTkFrame(master=app,
                             width=frame_side_length,
                             height=frame_side_length,
                             corner_radius=0,
                             fg_color="#ffd23f")
            frame.place(relx=0.4 + row * (padding / 800), rely=0.38 + col * (padding / 600))

            if state_str is None:
                entry = CTkEntry(master=frame,
                                 width=frame_side_length,
                                 height=frame_side_length,
                                 font=("Digital-7 Mono", 28, "bold"),
                                 text_color="#f3fcf0",
                                 border_color="#ffd23f",
                                 fg_color="#ffd23f")
                entry.place(relx=0.5, rely=0.5, anchor="center")
                entries.append(entry)
            else:
                idx = col * 3 + row
                value = state_str[idx]
                primary_color = "#f3fcf0"
                secondary_color = "red"
                if value == '0':
                    primary_color = secondary_color
                entry = CTkLabel(master=frame,
                                 width=frame_side_length,
                                 height=frame_side_length,
                                 font=("Digital-7 Mono", 28, "bold"),
                                 text=value,
                                 text_color=primary_color,
                                 fg_color="#ffd23f")
                entry.place(relx=0.5, rely=0.5, anchor="center")

    return entries


def is_valid(entries):
    try:
        state_str = ''.join(entry.get() for entry in entries)
        if not state_str.isdigit() or len(state_str) != 9:
            return False, state_str

        numbers = [int(x) for x in state_str]

        if sorted(numbers) != list(range(9)):
            return False, state_str

        if state_str == "123456780":
            return True, state_str

        numbers_without_zero = [x for x in numbers if x != 0]
        inversions = sum(1 for i in range(len(numbers_without_zero))
                         for j in range(i + 1, len(numbers_without_zero))
                         if numbers_without_zero[i] > numbers_without_zero[j])

        solvable = inversions % 2 == 0
        return solvable, state_str

    except ValueError:
        return False, ""


stop_sequence = False


def solve(app, algorithm, entries):
    global stop_sequence
    stop_sequence = False

    validation, state_str = is_valid(entries)

    if validation:
        ctk.CTkFrame(master=app,
                     height=50,
                     width=800,
                     fg_color="#540d6e").place(relx=0.5225, rely=0.3, anchor="center")

        ctk.CTkFrame(master=app,
                     height=200,
                     width=800,
                     fg_color="#540d6e").place(relx=0.5225, rely=0.9, anchor="center")

        stop_button = ctk.CTkButton(master=app,
                                    width=80,
                                    height=35,
                                    corner_radius=25,
                                    fg_color="#ffcc00",
                                    border_color="#c7ef00",
                                    hover_color="#a1286a",
                                    text="Stop",
                                    font=("Digital-7 Mono", 20, "bold"),
                                    command=stop_sequence_action)
        stop_button.place(relx=0.5225, rely=0.3, anchor="center")

        initial_board = string_to_board(state_str)

        if algorithm == "A*" and app.selected_heuristic.get() != "":
            states, moves, timeTaken, nodes = a_star(initial_board, app.selected_heuristic.get())
            show_steps(app, states, timeTaken, nodes, moves)
            states = [state[0] for state in states]
            show_states(app, states, 0)

        elif algorithm == "BFS":
            pass
            result = BFSAgent(initial_board).BFS_()
            show_steps(app, result[0], result[4], result[2], result[1])
            states = [str(state[0]).zfill(9) for state in result[0]]
            show_states(app, states, 0)

        elif algorithm == "DFS":
            result = DfsAgent(initial_board).dfs()
            if len(result[0]) > 30:
                create_step_viewer(app, result)
            else:
                show_steps(app, result[0], result[4], result[2], result[1])

            # states = [str(state[0]).zfill(9) for state in result[0]]
            # show_states(app, states[:51], 0)

        elif algorithm == "Iterative DFS":
            result = IdsAgent(initial_board).iterative_dfs()
            show_steps(app, result[0], result[4], result[2], result[1])
            states = [str(state[0]).zfill(9) for state in result[0]]
            show_states(app, states, 0)

        elif algorithm == "A*":
            show_optional_choices("A*", app)
            ctk.CTkLabel(master=app,
                         text="You must select a heuristic to solve the puzzle",
                         text_color="red",
                         font=("Digital-7 Mono", 28, "bold")).place(relx=0.5225, rely=0.9, anchor="center")

    else:
        ctk.CTkLabel(master=app,
                     text="Invalid Initial State",
                     text_color="red",
                     font=("Digital-7 Mono", 28, "bold")).place(relx=0.5225, rely=0.3, anchor="center")


def show_states(app, states, index, moves=None):
    if moves is None:
        moves = 0

    "#f78a53"
    ctk.CTkFrame(master=app,
                 corner_radius=0,
                 width=200,
                 height=50,
                 fg_color="#f78a53").place(relx=0.195, rely=0.5245, anchor="center")

    ctk.CTkFrame(master=app,
                 corner_radius=0,
                 width=200,
                 height=50,
                 fg_color="#ffd23f").place(relx=0.2, rely=0.53, anchor="center")

    ctk.CTkLabel(master=app,
                 text=f"Moves: {moves}",
                 text_color="white",
                 bg_color="#ffd23f",
                 font=("Digital-7 Mono", 28, "bold")).place(relx=0.2, rely=0.53, anchor="center")

    global stop_sequence
    if index < len(states) and not stop_sequence:
        show_board(app, 50, 70, states[index])

        if index < len(states) - 1:
            moves += 1

        app.after(1000, show_states, app, states, index + 1, moves)


def stop_sequence_action():
    global stop_sequence
    stop_sequence = True


def on_algorithm_change(choice):
    global selected_algorithm_result
    selected_algorithm_result = choice


def initiate_gui():
    app = CTk()
    app.geometry("800x600")
    app.configure(fg_color="#540d6e")

    title = ctk.CTkLabel(master=app, text="8 Puzzle AI Solver", font=("Digital-7 Mono", 28, "bold"))
    title.place(relx=0.5225, rely=0.075, anchor="center")

    option_algorithm = ctk.StringVar(value="")
    combobox = ctk.CTkComboBox(master=app,
                               width=200,
                               variable=option_algorithm,
                               values=["BFS", "DFS", "Iterative DFS", "A*"],
                               dropdown_font=("Digital-7 Mono", 18),
                               font=("Digital-7 Mono", 21, "bold"),
                               state="readonly",
                               command=lambda choice=option_algorithm.get(): show_optional_choices(choice, app))
    combobox.place(relx=0.5225, rely=0.15, anchor="center")

    entries = show_board(app, 50, 70)

    btn = ctk.CTkButton(master=app,
                        width=80,
                        height=35,
                        corner_radius=25,
                        fg_color="#ee4266",
                        border_color="#c7ef00",
                        hover_color="#a1286a",
                        text="Start",
                        font=("Digital-7 Mono", 20, "bold"),
                        command=lambda: solve(app, option_algorithm.get(), entries))
    btn.place(relx=0.5225, rely=0.22, anchor="center")

    app.mainloop()


initiate_gui()
