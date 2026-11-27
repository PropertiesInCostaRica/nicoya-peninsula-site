# Solo mira (no borra nada): que ocupa espacio en /var/log
import subprocess
def sh(c): return subprocess.run(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout.strip()
print('--- disco ---'); print(sh('df -h / | tail -1'))
print('--- total /var/log ---'); print(sh('du -sh /var/log 2>/dev/null'))
print('--- lo mas grande en /var/log ---'); print(sh('du -ah /var/log 2>/dev/null | sort -rh | head -25'))
print('--- logs viejos ya rotados (.gz, .1, .2 ...) ---'); print(sh("find /var/log -type f \\( -name '*.gz' -o -regex '.*\\.[0-9]+$' -o -regex '.*\\.[0-9]+\\.log$' \\) -printf '%s\\n' 2>/dev/null | awk '{s+=$1} END {printf \"%d archivos, %.0f MB\\n\", NR, s/1048576}'"))
print('--- journal del sistema ---'); print(sh('journalctl --disk-usage 2>/dev/null'))
print('--- correo de root (You have new mail) ---'); print(sh('ls -la /var/mail/root 2>/dev/null; grep -c "^From " /var/mail/root 2>/dev/null'))
print('LISTO (no se borro nada)')
