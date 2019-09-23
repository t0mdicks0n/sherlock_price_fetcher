spawn openvpn --config my_expressvpn_sweden_udp.ovpn
expect "*Enter Auth Username*"
send "j7zoptx3prdmpkjhtw2hrxcs\r"
expect "*Enter Auth Password*"
send "m617szobfpdg7bnzn23488tb\r"
expect eof