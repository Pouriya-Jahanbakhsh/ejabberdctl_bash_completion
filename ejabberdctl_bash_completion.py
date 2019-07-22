from sys import stdin

save_commands = False
commands = [('start',''), ('debug', '')]

for line in stdin:
    if line.startswith('Available commands'):
        save_commands = True
        continue
    elif line.startswith('Examples'):
        break
    if save_commands and len(line) > 4:
        if line[0:3] == '   ' and line[3].isalnum():
            command0 = tuple(line.strip().split(' ', 1))
            command = command0[0]
            if len(command0) == 2:
                arguments = command0[1]
            else:
                arguments = ''
            commands.append((command, arguments))

src = '''#! /usr/bin/env bash

__ejabberd_completion() {
    candidates=( '''
for command in commands:
    src += command[0] + ' '

src += ''' )
    for candidate in ${candidates[@]}; do
        if [[ "$candidate" == "${COMP_WORDS[1]}"* ]]; then
            COMPREPLY+=("$candidate")
        fi
    done
}

_ejabberd_completions() {
  COMPREPLY=()
  len=${#COMP_WORDS[@]}
  case "${COMP_WORDS[1]}" in
'''

for command in commands:
    command_case = '''\
      {})
          if [[ ${{len}} == 2 ]]; then
              COMPREPLY=("{}"){}
          elif [[ ${{len}} == 3 && ${{COMP_WORDS[-1]}} == "" ]]; then
              COMPREPLY=("{}")
          else
              return
          fi
          ;;
'''
    maybe_if = ''
    for item in commands:
        if len(item[0]) > len(command[0]) and item[0].startswith(command[0]):
            maybe_if = '''\

              __ejabberd_completion'''
    command_case = command_case.format(command[0], command[0] + ' ' + command[1], maybe_if, command[1])
    src += command_case

src += '''\
      *)
          __ejabberd_completion
  esac
}
complete -F _ejabberd_completions ejabberdctl
'''

print(src)
