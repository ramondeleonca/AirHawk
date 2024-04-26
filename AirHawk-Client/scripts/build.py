import subprocess as sp

def build():
    sp.run(["npm", "run", "build"], cwd="frontend", shell=True)

if __name__ == "__main__":
    build()