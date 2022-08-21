import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import argparse
import requests
from datetime import datetime, timezone
import os

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--report_path', dest='report_path', action='append', help='Path to crash report file')
args = arg_parser.parse_args()

pastebin_api_url = 'https://pastebin.com/api/api_post.php'
github_issue_url = 'https://github.com/grafexteam/fnf-grafex/issues/new/choose'
thanks_message = """
Report link copied to clipboard.
Thanks for reporting error to us, you're helping to improve the engine!
"""


class GrafexCrashHandler(tk.Tk):
    def __init__(self, report_path: str):
        super().__init__()

        self.crash_handler_file = report_path

        if report_path is None or not os.path.exists(self.crash_handler_file):
            raise Exception('Invalid crash report file path')

        with open(file=self.crash_handler_file, mode='r', encoding='UTF-8', newline='') as handle:
            self.error_message = handle.read()

        self.title('Grafex Engine: Crash Handler')
        self.geometry(f"{int(self.winfo_screenwidth() / 3)}x{int(self.winfo_screenheight() / 1.5)}")
        self.resizable(False, False)
        self.iconbitmap('resources/icon.ico')
        self.update()
        self.logo_img = ImageTk.PhotoImage(Image.open("resources/logo.png").resize((int(self.winfo_width() / 2),
                                                                                    int(self.winfo_height() / 4))))

        logo = tk.Label(master=self, image=self.logo_img)
        logo.pack(side=tk.TOP, pady=5)

        self.update()

        text = tk.Text(master=self, height=int((self.winfo_height() - logo.winfo_height()) / 22),
                       width=self.winfo_width() - 5, wrap=tk.NONE, font=('Consolas', 12))

        vertical_scroll = tk.Scrollbar(master=self)
        text.configure(yscrollcommand=vertical_scroll.set)

        horizontal_scroll = tk.Scrollbar(master=self, orient=tk.HORIZONTAL)
        text.configure(xscrollcommand=horizontal_scroll.set)

        text.insert(tk.END, self.error_message)
        text.configure(state='disabled')
        text.pack(side=tk.TOP, padx=5)
        horizontal_scroll.config(command=text.xview)
        vertical_scroll.config(command=text.yview)
        horizontal_scroll.pack(side=tk.TOP, fill=tk.X, padx=5)

        send_crash_btn = tk.Button(master=self, text='Send Crash Report', command=self.send_crash_report,
                                   width=15, bd=2)
        send_crash_btn.pack(side=tk.LEFT, padx=100, pady=5)

        close_handler = tk.Button(master=self, text='Close Game', command=self.close_handler,
                                  width=15, bd=2)
        close_handler.pack(side=tk.RIGHT, padx=100)

    def send_crash_report(self):
        request_params = {
            'api_dev_key': '2db6612f4ca1086310d8a1964c7fb1c0',
            'api_paste_code': self.error_message,
            'api_option': 'paste',
            'api_paste_name': f"Grafex Engine Crash Report: {datetime.now(tz=timezone.utc).strftime('%d.%m.%Y %H:%M')}",
            'api_paste_expire_date': '1M'
        }
        request = requests.post(url=pastebin_api_url, data=request_params)
        self.clipboard_clear()
        self.clipboard_append(str(request.text))
        os.system(f"start {github_issue_url}")
        messagebox.showinfo(title='Grafex Engine: Crash Handler', message=thanks_message)
        self.close_handler()

    def close_handler(self):
        self.destroy()
        exit()


if __name__ == "__main__":
    if not args.report_path:
        raise Exception('Invalid crash report file path')

    CrashHandler = GrafexCrashHandler(args.report_path[0])
    CrashHandler.mainloop()
