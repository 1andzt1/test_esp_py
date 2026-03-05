print ("--Start boot.py--")

# ---------- Запуск WebREPL ----------
try:
    import webrepl
    webrepl.start()
except Exception as e:
    print("WebREPL error:", e)

print("--End boot.py--")