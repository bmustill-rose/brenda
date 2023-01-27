import subprocess

def construct_command(binary_name, arguments, pattern):
 args = []
 args.append(binary_name)
 args.append("sendir")
 if arguments:
  for argument in arguments:
   args.append(argument)
 args.append(f"--pattern={pattern}")
 return args

def send_ir(path, binary_name, arguments, patterns):
 for pattern in patterns:
  command = construct_command(binary_name, arguments, pattern)
  subprocess.run(command, cwd=path)
