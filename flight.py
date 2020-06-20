from remote import AndroidRemote

remoteCtrl = AndroidRemote()

print('start_server:: Ready')
while True:
  state = remoteCtrl.get_data()
  print(state)
  