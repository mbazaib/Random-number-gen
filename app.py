import tkinter as tk
from tkinter import messagebox
import re
from itertools import permutations
import traceback
import os

# Basic user database
USER_DB = {
    "admin": "1234",
    "user": "pass"
}

class SecureGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Number Generator")
        self.root.config(bg="#f0f2f5") 
        
        self.generated_numbers_list = []
        
        self.container = tk.Frame(self.root, bg="#f0f2f5")
        self.container.pack(expand=True, fill="both")
        
        self.create_login_screen()

    def create_login_screen(self):
        self.login_card = tk.Frame(self.container, bg="white", padx=30, pady=30, relief="flat")
        self.login_card.pack(expand=True, pady=50)
        
        tk.Label(self.login_card, text="Secure Generator", font=("Helvetica", 20, "bold"), bg="white", fg="#333333").pack(pady=(0, 5))
        tk.Label(self.login_card, text="Please log in to continue", font=("Helvetica", 10), bg="white", fg="#777777").pack(pady=(0, 20))
        
        tk.Label(self.login_card, text="Username", font=("Helvetica", 10, "bold"), bg="white", fg="#555555").pack(anchor="w")
        self.username_entry = tk.Entry(self.login_card, font=("Arial", 14), bg="#f9f9f9", relief="solid", bd=1)
        self.username_entry.pack(fill="x", pady=(5, 15))
        
        tk.Label(self.login_card, text="Password", font=("Helvetica", 10, "bold"), bg="white", fg="#555555").pack(anchor="w")
        self.password_entry = tk.Entry(self.login_card, show="*", font=("Arial", 14), bg="#f9f9f9", relief="solid", bd=1)
        self.password_entry.pack(fill="x", pady=(5, 20))
        
        tk.Button(self.login_card, text="LOGIN", command=self.authenticate, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"), relief="flat", pady=10).pack(fill="x")

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username in USER_DB and USER_DB[username] == password:
            messagebox.showinfo("Success", f"Access Granted.\nWelcome, {username}!")
            self.login_card.destroy() 
            self.create_main_screen() 
        else:
            messagebox.showerror("Access Denied", "Invalid username or password.")

    def create_main_screen(self):
        self.main_frame = tk.Frame(self.container, bg="#f0f2f5")
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        tk.Label(self.main_frame, text="--- Generator Engine Active ---", font=("Helvetica", 14, "bold"), bg="#f0f2f5", fg="#333333").pack(pady=10)
        
        input_frame = tk.Frame(self.main_frame, bg="#f0f2f5")
        input_frame.pack(fill="x", pady=5)
        
        tk.Label(input_frame, text="10-Digit Base:", bg="#f0f2f5", font=("Helvetica", 10, "bold")).pack(side="left")
        self.number_entry = tk.Entry(input_frame, font=("Arial", 14), relief="solid", bd=1)
        self.number_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        tk.Button(self.main_frame, text="Generate Sequences", command=self.generate_sequences, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), relief="flat", pady=5).pack(pady=10)
        
        # Pinned Bottom Buttons
        action_frame = tk.Frame(self.main_frame, bg="#f0f2f5")
        action_frame.pack(side="bottom", fill="x", pady=5)
        
        tk.Button(action_frame, text="Copy All", command=self.copy_all_text, bg="#FF9800", fg="white", font=("Helvetica", 11, "bold"), relief="flat", pady=5).pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(action_frame, text="Save File", command=self.save_to_file, bg="#9C27B0", fg="white", font=("Helvetica", 11, "bold"), relief="flat", pady=5).pack(side="right", fill="x", expand=True, padx=5)

        # Expanding Output Frame
        output_frame = tk.Frame(self.main_frame, bg="#f0f2f5")
        output_frame.pack(side="top", expand=True, fill="both", pady=5)
        
        scrollbar = tk.Scrollbar(output_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.output_text = tk.Text(output_frame, yscrollcommand=scrollbar.set, font=("Courier", 11), state="disabled", relief="solid", bd=1)
        self.output_text.pack(expand=True, fill="both")
        scrollbar.config(command=self.output_text.yview)

    def copy_all_text(self):
        self.output_text.config(state="normal")
        content = self.output_text.get(1.0, tk.END).strip()
        self.output_text.config(state="disabled")
        
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            messagebox.showinfo("Copied!", "All generated numbers have been copied to your clipboard.")
        else:
            messagebox.showwarning("Empty", "There is nothing to copy yet.")

    def save_to_file(self):
        self.output_text.config(state="normal")
        content = self.output_text.get(1.0, tk.END).strip()
        self.output_text.config(state="disabled")
        
        if not content:
            messagebox.showwarning("Empty", "There are no numbers to save yet.")
            return

        # Smart cleaner: Ignores system notes and spacing break numbers when exporting
        lines = content.split('\n')
        api_ready_numbers = []
        for line in lines:
            clean_line = line.strip()
            # Skip lines that are just spacing marker numbers (e.g., "1", "2", "3") or system headers
            if clean_line.isdigit() or "[" in clean_line or not clean_line:
                continue
            
            if len(clean_line) == 10 and clean_line.isdigit():
                api_ready_numbers.append(clean_line)

        if not api_ready_numbers:
            messagebox.showwarning("Error", "No valid 10-digit numbers found in the output.")
            return

        try:
            file_name = "whatsapp_numbers.txt"
            with open(file_name, "w") as file:
                file.write("\n".join(api_ready_numbers))
            
            file_path = os.path.abspath(file_name)
            messagebox.showinfo("Saved!", f"Successfully saved {len(api_ready_numbers)} numbers for API use!\n\nLocation: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save the file: {str(e)}")

    def print_to_output(self, text):
        self.output_text.config(state="normal")
        self.output_text.insert(tk.END, text)
        self.output_text.config(state="disabled")
        self.output_text.see(tk.END)

    def generate_sequences(self):
        clean_num = self.number_entry.get().replace(" ", "")
        
        if len(clean_num) != 10 or not clean_num.isdigit():
            messagebox.showerror("Error", "The number must have exactly 10 digits.")
            return

        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state="disabled")
        
        self.print_to_output(f"[System] Running sequence on base: {clean_num}...\n\n")

        seen_numbers = set()
        self.generated_numbers_list = []
        print_count = 0 
        break_counter = 1  # Counter for the numbers on line breaks

        def print_unique(new_num):
            nonlocal print_count, break_counter
            if new_num not in seen_numbers:
                seen_numbers.add(new_num)
                self.generated_numbers_list.append(new_num)
                self.print_to_output(new_num + "\n")
                print_count += 1
                
                # Whenever we hit a multiple of 5, print a sequential number on the break line instead of blank space
                if print_count % 5 == 0:
                    self.print_to_output(f"{break_counter}\n")
                    break_counter += 1

        print_unique(clean_num)

        # ==========================================
        # PART 1: Modifying Specific Positions
        # ==========================================
        offsets = [1, 2, -1, -2]
        targets = [3, 4, 5, 6, 7, 8, 9] 
        
        for target_idx in targets:
            target_digit = int(clean_num[target_idx])
            for offset in offsets:
                new_digit = (target_digit + offset) % 10
                prefix = clean_num[:target_idx]
                suffix = clean_num[target_idx+1:]
                new_number = f"{prefix}{new_digit}{suffix}"
                print_unique(new_number)

        # ==========================================
        # PART 2: Shuffling Repeated Blocks
        # ==========================================
        prefix_3 = clean_num[:3]
        suffix_7 = clean_num[3:]
        
        matches = list(re.finditer(r'(\d)\1+', suffix_7))
        if len(matches) >= 2:
            block_values = [m.group() for m in matches]
            unique_perms = set(permutations(block_values))
            
            for perm in unique_perms:
                swapped_suffix = ""
                last_end = 0
                for i, match in enumerate(matches):
                    swapped_suffix += suffix_7[last_end:match.start()]
                    swapped_suffix += perm[i]
                    last_end = match.end()
                swapped_suffix += suffix_7[last_end:]
                swapped_num = prefix_3 + swapped_suffix
                print_unique(swapped_num)

        # ==========================================
        # PART 3: Swapping Adjacent Distinct Digits
        # ==========================================
        for i in range(3, len(clean_num) - 1):
            if clean_num[i] != clean_num[i+1]:
                swapped = clean_num[:i] + clean_num[i+1] + clean_num[i] + clean_num[i+2:]
                print_unique(swapped)

        # ==========================================
        # PART 4: Permuting 4-Digit Patterns
        # ==========================================
        for i in range(3, len(clean_num) - 3):
            window = clean_num[i:i+4]
            if len(set(window)) == 2 and all(window.count(c) == 2 for c in set(window)):
                perms = set(permutations(window))
                for p in perms:
                    p_str = "".join(p)
                    new_num = clean_num[:i] + p_str + clean_num[i+4:]
                    print_unique(new_num)

        # ==========================================
        # PART 5: Swapping Before/After 3 or 4-Digit Sequences
        # ==========================================
        all_matches = list(re.finditer(r'(\d)\1+', clean_num))
        for m in all_matches:
            seq = m.group()
            if 3 <= len(seq) <= 4:
                start_idx = m.start()
                end_idx = m.end()
                if (start_idx - 1) >= 3 and end_idx < len(clean_num):
                    before_idx = start_idx - 1
                    after_idx = end_idx
                    swapped = (
                        clean_num[:before_idx] +
                        clean_num[after_idx] +
                        clean_num[start_idx:end_idx] +
                        clean_num[before_idx] +
                        clean_num[after_idx+1:]
                    )
                    print_unique(swapped)

        # ==========================================
        # PART 6: Replacing 3 or 4-Digit Sequences with 0-9
        # ==========================================
        for m in all_matches:
            seq = m.group()
            if 3 <= len(seq) <= 4:
                start_idx = m.start()
                end_idx = m.end()
                if start_idx >= 3:
                    orig_digit = seq[0]
                    for d in range(10):
                        new_char = str(d)
                        if new_char != orig_digit:
                            new_seq = new_char * len(seq)
                            new_num = clean_num[:start_idx] + new_seq + clean_num[end_idx:]
                            print_unique(new_num)

        # ==========================================
        # PART 7: Modifying the 3rd Position to 0, 2, 4, 6, 8
        # ==========================================
        for even_digit in ['0', '2', '4', '6', '8']:
            new_num = clean_num[:2] + even_digit + clean_num[3:]
            print_unique(new_num)

        # ==========================================
        # PART 8: Replicating Generated Numbers with 3rd Position Changes (0, 2, 4, 5, 6, 8)
        # ==========================================
        base_generated_snapshot = list(seen_numbers)
        for num in base_generated_snapshot:
            for digit in ['0', '2', '4', '5', '6', '8']:
                modified_num = num[:2] + digit + num[3:]
                print_unique(modified_num)

        self.print_to_output(f"\n[System] Generation Complete. Total variations: {print_count}\n")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = SecureGeneratorApp(root)
        root.mainloop()
    except Exception as e:
        print("=== CRITICAL ERROR ===")
        print("The app crashed! Here is the reason why:")
        traceback.print_exc()
        print("\n======================")
        input("Press ENTER to close this window...")
