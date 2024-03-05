def acked(err, msg):
    if err is not None:
        print("Fallimento nella consegna del messaggio: %s: %s" %
              (str(msg), str(err)))
