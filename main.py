import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os
#Import style page for styling 
from styles import PRIMARY_COLOR, SECONDARY_COLOR, BG_COLOR, SPECIAL_BG_COLOR, TEXT_COLOR, FONT_DEFAULT, FONT_BOLD, FONT_ITALIC, TEXT_COLOR2, CONTROL_FRAME_COLOR
#Import dataload page for the main data could be used 
from dataload import column_ranges, sheet, city_names, city_points, map_points

# List of city names ordered by points
city_names_ordered = list(city_points.values())

# Function to read subtopics based on the selected main topic
def read_subtopics(main_topic):
    subtopics = []
    if main_topic in column_ranges:
        column_range = column_ranges[main_topic]
        for col_idx in column_range:
            subtopic = sheet.cell(row=1, column=col_idx).value
            if subtopic:
                subtopics.append(subtopic)
        if main_topic == 'Age' and 'Average Age' in subtopics:
            subtopics.remove('Average Age')
            subtopics.insert(0, 'Average Age')
    return subtopics

# Function to read data for a specific city and subtopic
def read_data(city_code, main_topic, subtopic):
    data = []
    main_topic_columns = column_ranges.get(main_topic, [])
    if main_topic_columns:
        subtopic_index = None
        for col_idx in main_topic_columns:
            if sheet.cell(row=1, column=col_idx).value == subtopic:
                subtopic_index = col_idx
                break
        if subtopic_index is not None:
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if row[1] == city_code:
                    year = row[0]
                    value = row[subtopic_index - 1]
                    if year in [2016, 2017, 2018, 2019]:
                        data.append((year, value))
    return data

# Function to read data for all cities for a specific subtopic
def read_data_for_all_cities(main_topic, subtopic):
    data = {}
    main_topic_columns = column_ranges.get(main_topic, [])
    if main_topic_columns:
        subtopic_index = None
        for col_idx in main_topic_columns:
            if sheet.cell(row=1, column=col_idx).value == subtopic:
                subtopic_index = col_idx
                break
        if subtopic_index is not None:
            for row in sheet.iter_rows(min_row=2, values_only=True):
                year = row[0]
                city_code = row[1]
                city_name = row[2]
                value = row[subtopic_index - 1]
                if year in [2016, 2017, 2018, 2019]:
                    if city_name not in data:
                        data[city_name] = []
                    data[city_name].append((year, value))
    return data

# Function to get all unique years from the dataset
def get_years():
    years = set()
    for main_topic in column_ranges.keys():
        for subtopic in read_subtopics(main_topic):
            data = read_data_for_all_cities(main_topic, subtopic)
            for city_data in data.values():
                for year, _ in city_data:
                    years.add(year)
    return sorted(list(years))

# Function to update the subtopic dropdown based on the selected main topic
def update_subtopics(event=None):
    selected_main_topic = topic_dropdown.get()
    subtopics = read_subtopics(selected_main_topic)
    subtopic_dropdown['values'] = subtopics
    subtopic_dropdown.current(0)
    update_info_text()

# Function to update the information text displayed
def update_info_text(event=None):
    selected_year = year_dropdown.get()
    main_topic = topic_dropdown.get().title()
    subtopic = subtopic_dropdown.get().title()

    info_text.config(state=tk.NORMAL)
    info_text.delete(1.0, tk.END)
    info_text.insert(tk.END, f"{selected_year} | {main_topic} | {subtopic}")
    info_text.config(state=tk.DISABLED)

# Function to handle city button hover event
def on_city_hover(event):
    city_name = event.widget.cget("text")
    main_topic = topic_dropdown.get()
    subtopic = subtopic_dropdown.get()
    year = year_dropdown.get()

    if city_name and main_topic and subtopic and year:
        data = read_data_for_all_cities(main_topic, subtopic)
        value = next((v for y, v in data.get(city_name, []) if y == int(year)), 'N/A')
        tooltip = f"{subtopic} ({year}): {value}"
        tooltip_label.config(text=tooltip)

# Function to handle mouse hover over city button
def on_hover(event, city):
    main_topic = topic_dropdown.get()
    subtopic = subtopic_dropdown.get()
    selected_year = int(year_dropdown.get())

    if main_topic and subtopic and selected_year:
        data = read_data_for_all_cities(main_topic, subtopic)
        value = next((value for y, value in data.get(city, []) if y == selected_year), 'N/A')
        tooltip = f"{city}: {value}"
        tooltip_label.place(x=event.x_root - window.winfo_rootx() + 10, y=event.y_root - window.winfo_rooty() + 10)
        tooltip_label.config(text=tooltip, bg='yellow', fg='black')

# Function to handle mouse leave event from city button
def on_leave(event):
    tooltip_label.place_forget()

# Function to create the main window and UI component
def create_main_window():
    global window, info_text, score_board
    window = tk.Tk()
    window.title("Data Viewer for Structure and Characteristics of Urban Areas in Rostock City")
    window.attributes("-fullscreen", True)  # Set full screen
    window.configure(bg=BG_COLOR)

    def exit_fullscreen(event=None):
        window.attributes("-fullscreen", False)

    window.bind("<Escape>", exit_fullscreen)  # Bind the escape key to exit full-screen mode

    # Control frame for dropdowns and info text
    control_frame = tk.Frame(window, bg=BG_COLOR, padx=20, pady=20)
    control_frame.pack(side=tk.TOP, fill=tk.X)

    # Content frame to hold display and image frames
    content_frame = tk.Frame(window, bg=BG_COLOR)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Display frame for score board and graphs
    display_frame = tk.Frame(content_frame, bg=SPECIAL_BG_COLOR, bd=5, relief=tk.SUNKEN)
    display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)

    # Image frame for the map
    image_frame = tk.Frame(content_frame, bg=SPECIAL_BG_COLOR, bd=5, relief=tk.SUNKEN)
    image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20)

    # Scoreboard for displaying high and low values
    score_board = tk.Frame(display_frame, bg='light grey', border=10, borderwidth=4, highlightthickness=5,  # Thickness of the border
    relief="solid" )
    
    score_board.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=40, padx=80)

    # Scoreboard title label
    title_label = tk.Label(score_board, text="SCORE BOARD", bg='light green', fg=TEXT_COLOR, font=('Helvetica', 15))
    title_label.pack(fill=tk.X)

    high_value_label = tk.Label(score_board, text="", bg='maroon', fg='white', font=(FONT_DEFAULT[0], 15))
    high_value_label.pack(pady=10) 
    high_value_label.pack(fill=tk.X)

    low_value_label = tk.Label(score_board, text="", bg='yellow', fg='black', font=(FONT_DEFAULT[0], 15))
    low_value_label.pack(pady=10) 
    low_value_label.pack(fill=tk.X)

    # Graph frame for data visualization
    graph_frame = tk.Frame(display_frame, bg=SPECIAL_BG_COLOR)
    graph_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # Labels and dropdowns for user controls
    city_label = tk.Label(control_frame, text="Select First Area:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_BOLD)
    city_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

    selected_city1 = tk.StringVar()
    city_dropdown1 = ttk.Combobox(control_frame, textvariable=selected_city1, values=list(city_names.values()), width=30, font=FONT_DEFAULT)
    city_dropdown1.grid(row=0, column=1, padx=10, pady=5)
    city_dropdown1.current(0)

    city_label2 = tk.Label(control_frame, text="Select Second Area:", bg=CONTROL_FRAME_COLOR, fg=TEXT_COLOR2, font=FONT_BOLD)
    city_label2.grid(row=1, column=0, padx=10, pady=5, sticky='w')

    selected_city2 = tk.StringVar()
    city_dropdown2 = ttk.Combobox(control_frame, textvariable=selected_city2, values=['Compare with second city'] + list(city_names.values()), width=30, font=FONT_DEFAULT)
    city_dropdown2.grid(row=1, column=1, padx=10, pady=5)
    city_dropdown2.current(0)

    style = ttk.Style()
    style.configure('TCombobox', foreground='black', background=TEXT_COLOR, fieldbackground=TEXT_COLOR, font=FONT_ITALIC)

    main_topic_label = tk.Label(control_frame, text="Select the Main Topic:", bg=CONTROL_FRAME_COLOR, fg=TEXT_COLOR2, font=FONT_BOLD)
    main_topic_label.grid(row=0, column=2, padx=10, pady=5, sticky='w')

    selected_topic = tk.StringVar()
    global topic_dropdown
    topic_dropdown = ttk.Combobox(control_frame, textvariable=selected_topic, width=30, font=FONT_DEFAULT)
    topic_dropdown.grid(row=0, column=3, padx=10, pady=5)
    topic_dropdown.bind("<<ComboboxSelected>>", update_subtopics)

    main_topics = list(column_ranges.keys())
    topic_dropdown['values'] = main_topics
    topic_dropdown.current(0)

    year_label = tk.Label(control_frame, text="Select the Year:", bg=CONTROL_FRAME_COLOR, fg=TEXT_COLOR2, font=FONT_BOLD)
    year_label.grid(row=0, column=4, padx=10, pady=5, sticky='w')

    selected_year = tk.StringVar()
    global year_dropdown
    year_dropdown = ttk.Combobox(control_frame, textvariable=selected_year, width=30, font=FONT_DEFAULT)
    year_dropdown.grid(row=0, column=5, padx=10, pady=5)
    year_dropdown.bind("<<ComboboxSelected>>", update_info_text)

    years = get_years()
    year_dropdown['values'] = years
    year_dropdown.current(0)

    subtopic_label = tk.Label(control_frame, text="Select the Subtopic:", bg=CONTROL_FRAME_COLOR, fg=TEXT_COLOR2, font=FONT_BOLD)
    subtopic_label.grid(row=1, column=2, padx=10, pady=5, sticky='w')

    selected_subtopic = tk.StringVar()
    global subtopic_dropdown
    subtopic_dropdown = ttk.Combobox(control_frame, textvariable=selected_subtopic, values=[], width=30, font=FONT_DEFAULT)
    subtopic_dropdown.grid(row=1, column=3, padx=10, pady=5)
    subtopic_dropdown.bind("<<ComboboxSelected>>", update_info_text)

    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Create a frame for the info text and the button
    info_and_button_frame = tk.Frame(image_frame, bg=SPECIAL_BG_COLOR)
    info_and_button_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

    info_text = tk.Text(info_and_button_frame, height=1, width=45, wrap=tk.WORD, bg='light green', fg=TEXT_COLOR, font=FONT_BOLD, bd=2, relief=tk.SUNKEN, padx=10, pady=10)
    info_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
    info_text.insert(tk.END, "")
    info_text.config(state=tk.DISABLED)

    go_to_graph_button = tk.Button(info_and_button_frame, text="Go to Graph", command=lambda: show_all_cities_data(), bg=SECONDARY_COLOR, fg="white", font=FONT_BOLD)
    go_to_graph_button.pack(side=tk.RIGHT, padx=10)

    def load_image():
        try:
            image_path = "Rostock.jpg"
            if os.path.exists(image_path):
                image = Image.open(image_path)
                image = image.resize((600, 600), Image.LANCZOS)
                tk_image = ImageTk.PhotoImage(image)
                image_label = tk.Label(image_frame, image=tk_image)
                image_label.image = tk_image
                image_label.pack()

                image_label.pack(expand=True, fill="both")
                
                for point, city in zip(map_points, city_names_ordered):
                    pin = tk.Label(image_frame, text='📍', bg='maroon', fg='white')
                    pin.place(x=point[0], y=point[1])
                    pin.bind("<Enter>", lambda event, c=city: on_hover(event, c))
                    pin.bind("<Leave>", on_leave)

            else:
                print(f"Error: Image file '{image_path}' not found.")
        except Exception as e:
            print(f"Error: {e}")

    load_image()
    update_subtopics()

    def show_data():
        city_code1 = next((key for key, value in city_names.items() if value == selected_city1.get()), None)
        city_code2 = next((key for key, value in city_names.items() if value == selected_city2.get()), None) if selected_city2.get() != 'Compare with second city' else None
        main_topic = topic_dropdown.get()
        subtopic = subtopic_dropdown.get()
        selected_year = int(year_dropdown.get())

        high_value_label.config(text="")
        low_value_label.config(text="")
        ax.clear()

        if city_code1 and main_topic and subtopic:
            data1 = read_data(city_code1, main_topic, subtopic)
            data2 = read_data(city_code2, main_topic, subtopic) if city_code2 else []

            years1 = [year for year, value in data1]
            values1 = [value for year, value in data1]
            years2 = [year for year, value in data2] if city_code2 else []
            values2 = [value for year, value in data2] if city_code2 else []

            data_all_cities = read_data_for_all_cities(main_topic, subtopic)
            values_for_year = {city: next((value for y, value in city_data if y == selected_year), None) for city, city_data in data_all_cities.items()}
            values_for_year = {city: value for city, value in values_for_year.items() if value is not None}

            if values_for_year:
                max_city = max(values_for_year, key=values_for_year.get)
                min_city = min(values_for_year, key=values_for_year.get)

                max_city_value = values_for_year[max_city]
                min_city_value = values_for_year[min_city]

                high_value_label.config(text=f"Highest Value: {max_city}; {max_city_value}")
                low_value_label.config(text=f"Lowest Value: {min_city}; {min_city_value}")

            bar_width = 0.3
            bar_positions1 = np.arange(len(years1)) * 2
            bar_positions2 = bar_positions1 + bar_width

            ax.bar(bar_positions1, values1, color=SECONDARY_COLOR, alpha=0.7, width=bar_width, label=city_names[city_code1])
            if city_code2:
                ax.bar(bar_positions2, values2, color=PRIMARY_COLOR, alpha=0.7, width=bar_width, label=city_names[city_code2])

            if years1 and values1:
                ax.plot(bar_positions1, values1, marker='o', color='b', linestyle='-', label=f"{city_names[city_code1]} Trend", markersize=2)
            if years2 and values2:
                ax.plot(bar_positions2, values2, marker='o', color='g', linestyle='-', label=f"{city_names[city_code2]} Trend", markersize=2)

            offset = 0.02 * max(max(values1, default=0), max(values2, default=0))
            for i, v in enumerate(values1):
                ax.text(bar_positions1[i], v + offset, str(v), ha='center', va='bottom', fontsize=10)
            if city_code2:
                for i, v in enumerate(values2):
                    ax.text(bar_positions2[i], v + offset, str(v), ha='center', va='bottom', fontsize=10)

            ax.yaxis.grid(True, linestyle='--', linewidth=0.7, alpha=0.7)

            ax.set_title(f"{main_topic}: {subtopic}")
            ax.set_xlabel("Year")
            ax.set_ylabel(subtopic)
            ax.set_xticks(bar_positions1 + bar_width / 2)
            ax.set_xticklabels([str(year) for year in years1])
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

            fig.tight_layout()

            canvas.draw()
        else:
            if not city_code1:
                high_value_label.config(text="Please select City 1.")
            if not main_topic:
                low_value_label.config(text="Please select a Main Topic.")
            if not subtopic:
                low_value_label.config(text="Please select a Subtopic.")

    def show_all_cities_data():
        main_topic = topic_dropdown.get()
        subtopic = subtopic_dropdown.get()
        selected_year = int(year_dropdown.get())
        data = read_data_for_all_cities(main_topic, subtopic)

        if data:
            all_cities_window = tk.Toplevel(window)
            all_cities_window.title(f"All Cities Data for {subtopic} in {selected_year}")
            all_cities_window.geometry("1200x800")
            all_cities_window.configure(bg=BG_COLOR)

            fig_all = Figure(figsize=(10, 6), dpi=100)
            ax_all = fig_all.add_subplot(111)
            canvas_all = FigureCanvasTkAgg(fig_all, master=all_cities_window)
            canvas_all.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            cities = list(data.keys())
            bar_width = 0.5
            bar_positions = np.arange(len(cities))

            values = [next((value for y, value in data[city_name] if y == selected_year), 'N/A') for city_name in cities]
            bars = ax_all.bar(bar_positions, values, width=bar_width, color=SECONDARY_COLOR, alpha=0.7)

            offset = 0.02 * max(max(values, default=0), 0)
            for bar in bars:
                height = bar.get_height()
                ax_all.text(bar.get_x() + bar.get_width() / 2, height + offset, str(height), ha='center', va='bottom', fontsize=8)

            ax_all.set_title(f"All Cities - {main_topic}: {subtopic} ({selected_year})")
            ax_all.set_xlabel("Cities")
            ax_all.set_ylabel(subtopic)
            ax_all.set_xticks(bar_positions)
            ax_all.set_xticklabels(cities, rotation=45, ha="right")
            ax_all.legend(loc='center left', bbox_to_anchor=(1, 0.5))

            ax_all.yaxis.grid(True, linestyle='--', linewidth=0.7, alpha=0.7)

            fig_all.tight_layout()

            canvas_all.draw()
        else:
            high_value_label.config(text="No data found for any city.")

    show_data_button = tk.Button(control_frame, text="Show Data", command=show_data, bg=PRIMARY_COLOR, fg="white", width=20, font=FONT_BOLD)
    show_data_button.grid(row=2, column=2, padx=10, pady=10, sticky='e')

    global tooltip_label
    tooltip_label = tk.Label(window, text="", bg=SPECIAL_BG_COLOR, fg=TEXT_COLOR, font=FONT_DEFAULT)
    tooltip_label.pack_forget()

    window.mainloop()

if __name__ == "__main__":
    create_main_window()
