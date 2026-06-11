import re

with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Extract the KCP block
kcp_start = text.find('<!-- Visão KCP Expert -->')
if kcp_start == -1:
    print("Could not find KCP block")
    exit(1)

kcp_end = text.find('<div id="s-vs"', kcp_start)
if kcp_end == -1:
    print("Could not find s-vs")
    exit(1)

# Extract and remove
kcp_block = text[kcp_start:kcp_end]
text = text[:kcp_start] + text[kcp_end:]

# 2. Find the END of s-oque
# s-oque starts here:
soque_idx = text.find('id="s-oque"')
# The next section after it is s-vs
svs_idx = text.find('<div id="s-vs"')

# The closing div of s-oque should be right before svs_idx (and before <!-- ===== VS ===== -->)
# Let's find <!-- ===== VS ===== -->
vs_marker = text.find('<!-- ===== VS ===== -->', soque_idx)
if vs_marker == -1:
    print("Could not find VS marker")
    exit(1)

# So the end of s-oque is right before vs_marker. We'll insert it there.
# Wait, s-oque might have a closing </div> right before vs_marker.
# If we insert it before the last </div> of s-oque, it will be inside s-oque.
# Let's just find the last </div> before vs_marker.
last_div_close = text.rfind('</div>', soque_idx, vs_marker)

if last_div_close != -1:
    text = text[:last_div_close] + "\n" + kcp_block + "\n" + text[last_div_close:]
    with open('contexto/scrumban_guia.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed KCP placement!")
else:
    print("Could not find closing div")
