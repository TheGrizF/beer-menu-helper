import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
READ_ONLY_TOKEN = os.getenv('UTFB_READ_ONLY_TOKEN')
EMAIL = os.getenv('EMAIL')
UTFB_API_URL = 'https://business.untappd.com/api/v1/items/search.json'


translation_table = str.maketrans({
    "’": "'",
    "‘": "'",
    "“": '"',
    "”": '"',
    "—": "-",
    "–": "-"
})


class BeerMenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bulk Beer CSV Generator with Untappd")

        self.containers = [
            ('4-pack 16oz Cans', 6),
            ('4-pack 12oz Cans', 6),
            ('6-pack 12oz Cans', 4),
            ('16oz Can (Single)', 24),
            ('12oz Can (Single)', 24),
            ('375ml Bottle', 12),
            ('500ml Bottle', 12),
            ('750ml Bottle', 12),
            ('22oz Bottle', 12)
        ]
        self.beer_entries = []
        self.added_names = set()

        left_frame = tk.Frame(root)
        left_frame.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(left_frame, text="Beer Name:").grid(row=0, column=0, padx=(0, 5), pady=5, sticky='e')
        self.beer_name_entry = tk.Entry(left_frame, width=40)
        self.beer_name_entry.grid(row=0, column=1, pady=5, sticky='w')

        tk.Label(left_frame, text="Container:").grid(row=1, column=0, sticky='e')
        self.container_var = tk.StringVar()
        container_options = [c[0] for c in self.containers]
        self.container_dropdown = ttk.Combobox(left_frame, textvariable=self.container_var, values=container_options)
        self.container_dropdown.current(0)
        self.container_dropdown.grid(row=1, column=1, sticky='w')
        self.container_dropdown.bind('<<ComboboxSelected>>', lambda event: self.calculate_suggested_price())
        
        tk.Label(left_frame, text="Case Cost:").grid(row=2, column=0, sticky='e')
        self.case_cost_entry = tk.Entry(left_frame, width=10)
        self.case_cost_entry.grid(row=2, column=1, pady=5, sticky='w')
        self.case_cost_entry.bind('<KeyRelease>', lambda event: self.calculate_suggested_price())

        self.price_suggestion = tk.StringVar()
        tk.Label(left_frame, text="Suggested Price:").grid(row=3, column=0, sticky='e')
        self.suggestion_label = tk.Label(left_frame, textvariable=self.price_suggestion)
        self.suggestion_label.grid(row=3, column=1, sticky='w')

        tk.Label(left_frame, text="Set Price ($):").grid(row=4, column=0, sticky='e')
        self.price_entry = tk.Entry(left_frame, width=10)
        self.price_entry.grid(row=4, column=1, pady=5, sticky='w')

        self.preview_button = tk.Button(left_frame, text="Search", command=self.preview_beer)
        self.preview_button.grid(row=5, column=0, pady=10)

        self.add_button = tk.Button(left_frame, text="Add to Bulk List", command=self.add_beer)
        self.add_button.grid(row=5, column=1, pady=10)

        tk.Label(left_frame, text="Preview:").grid(row=6, column=0, columnspan=2)
        self.output_text = tk.Text(left_frame, height=12, width=60)
        self.output_text.grid(row=7, column=0, columnspan=2, pady=5)

        self.save_button = tk.Button(left_frame, text="Generate CSV", command=self.save_to_csv)
        self.save_button.grid(row=8, column=0, columnspan=2, pady=10)


        right_frame = tk.Frame(root)
        right_frame.grid(row=0, column=1, padx=10, sticky='n')

        tk.Label(right_frame, text="Current Beers:").pack()
        self.added_listbox = tk.Listbox(right_frame, height=25, width=50)
        self.added_listbox.pack(padx=5, pady=5)

        self.remove_button = tk.Button(right_frame, text="Remove Selected", command=self.remove_selected_entry)
        self.remove_button.pack(pady=5)

    def calculate_suggested_price(self):
        try:
            case_cost = float(self.case_cost_entry.get())
            container_qty = next((c[1] for c in self.containers if c[0] == self.container_var.get()), 1)
            unit_cost = case_cost / container_qty
            price_low = unit_cost * 1.4
            price_high = unit_cost * 1.5
            self.price_suggestion.set(f"${price_low:.2f} - ${price_high:.2f}")
        except ValueError:
            self.price_suggestion.set("Enter valid cost")
    
    def search_untappd(self, beer_name: str):
        headers = {'Accept': 'application/json'}
        params = {'q': beer_name}
        response = requests.get(
            UTFB_API_URL,
            auth=HTTPBasicAuth(EMAIL, READ_ONLY_TOKEN),
            headers=headers,
            params=params
        )

        if response.status_code == 200:
            data = response.json()
            beers = []
            for beer in data['items']:
                beers.append({
                    'name': beer['name'].translate(translation_table),
                    'brewery': beer['brewery'].translate(translation_table),
                    'abv': beer['abv'],
                    'style': beer['style'].translate(translation_table),
                    'description': beer['description'].translate(translation_table)
                })
            return beers
        else:
            messagebox.showerror("API Error", f"{response.status_code} - {response.text}")
            return []

    def preview_beer(self):
        self.output_text.delete(1.0, tk.END)
        self.current_preview = None

        beer_name = self.beer_name_entry.get()
        beers = self.search_untappd(beer_name)

        if not beers:
            messagebox.showerror("No Results", "Not found on Untappd.")
            return
        
        top = beers[0]
        msg = (f"Found {len(beers)} results:"
               f"{top['brewery']} {top['name']}\n{top['abv']}% {top['style']}\n\n"
               "Use this entry?")
        
        if messagebox.askyesno("Search Result", msg):
            self.show_selected_beer(top)
        else:
            self.show_selection_window(beers)

    def show_selection_window(self, beers):
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.title("Results from Untappd")

        tk.Label(self.selection_window, text="Select entry:").pack(pady=5)
        self.selected_beer = tk.StringVar()

        for b in beers:
            display = f"{b['brewery']} - {b['name']} {b['abv']}% {b['style']}"
            tk.Radiobutton(self.selection_window, text=display, variable=self.selected_beer, value=b['name']).pack(anchor='w')

        tk.Button(self.selection_window, text="Select", command=lambda: self.confirm_selection(beers)).pack(pady=5)
    
    def confirm_selection(self, beers):
        selected = self.selected_beer.get()
        if not selected:
            messagebox.showerror("Selection Error", "Make a selection.")
            return
        beer = next((b for b in beers if b['name'] == selected), None)
        if beer:
            self.show_selected_beer(beer)
        self.selection_window.destroy()

    def show_selected_beer(self, beer):
        self.current_preview = beer
        container_choice = self.container_var.get()
        description = f"{container_choice} {beer['abv']}% abv {beer['style']}\n{beer['description']}"
        description = description[:1000]

        self.output_text.insert(tk.END, f"Preview:\n{beer['brewery']} {beer['name']} {beer['abv']}% {beer['style']}\n{description}\n\n")

    def add_beer(self):
        if not self.current_preview:
            messagebox.showerror("Error", "Please preview a beer first.")
            return

        try:
            user_price = float(self.price_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Enter a valid price.")
            return

        beer = self.current_preview
        full_name = f"{beer['brewery']} {beer['name']}"
        pos_name = f"{beer['brewery'].split()[0]} {beer['name']}" if len(beer['brewery']) > 10 else ''
        container_choice = self.container_var.get()
        description = f"\"{container_choice} {beer['abv']}% abv {beer['style']}\n{beer['description']}\""
        description = description[:997]

        if full_name in self.added_names:
            messagebox.showinfo("Duplicate", f"{full_name} has already been added.")
            return

        row = {
            'Name': full_name,
            'Price': user_price,
            'POS Name': pos_name,
            'Kitchen Name': '',
            'Description': description,
            'Calories': '',
            'SKU': '',
            'PLU': ''
        }

        self.added_names.add(full_name)
        display = f"{full_name} - ${user_price:.2f}"
        self.added_listbox.insert(tk.END, display)
        self.beer_entries.append(row)
        self.output_text.insert(tk.END, f"Added: {full_name} at ${user_price:.2f}\n\n")

    def remove_selected_entry(self):
        selection = self.added_listbox.curselection()
        if not selection:
            messagebox.showinfo("No Selection", "Select an beer to remove.")
            return
        
        index = selection[0]
        entry = self.added_listbox.get(index)
        name = entry.rsplit(" - $", 1)[0]
        self.added_listbox.delete(index)

        self.beer_entries = [row for row in self.beer_entries if row['Name'] != name]
        self.added_names.discard(name)

        self.output_text.insert(tk.END, f"Removed: {name}\n\n")

    def save_to_csv(self):
        if not self.beer_entries:
            messagebox.showerror("No Data", "No beers to save.")
            return

        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save CSV")
        if file:
            keys = ['Name', 'Price', 'POS Name', 'Kitchen Name',
                    'Description', 'Calories', 'SKU', 'PLU']
            with open(file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=keys)
                writer.writeheader()
                writer.writerows(self.beer_entries)
            messagebox.showinfo("Success", f"Saved {len(self.beer_entries)} items to CSV.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BeerMenuApp(root)
    root.mainloop()