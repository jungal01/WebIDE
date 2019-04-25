import subprocess
import unittest


class TestCompiling(unittest.TestCase):

    def compile_file(self, language, file, platform="default"):
        command = "../../call-compiler {0} --platform={1} {2}" .format(language, platform, file)
        subprocess.run(command, shell=True)

    def test_python(self):
        self.compile_file("python", "hello.py")
        file = open('output.txt')
        x = file.read()
        self.assertTrue("Hello Python" in x)
        file.close()

    def test_java(self):
        self.compile_file("java", "hello.java")
        file = open('output.txt')
        x = file.read()
        self.assertTrue("Hello Java" in x)
        file.close()

    def test_js(self):
        self.compile_file("js", "hello.js")
        file = open('output.txt')
        x = file.read()
        self.assertTrue("Hello JS" in x)
        file.close()

    def test_lua(self):
        self.compile_file("lua", "hello.lua")
        file = open('output.txt')
        x = file.read()
        self.assertTrue("Hello Lua" in x)
        file.close()

    def test_ruby(self):
        self.compile_file("ruby", "hello.rb")
        file = open('output.txt')
        x = file.read()
        self.assertTrue("Hello Ruby" in x)
        file.close()

    def test_bash(self):
        self.compile_file("bash", "hello.sh")
        file = open('output.txt')
        x = file.read()
        self.assertTrue("Hello Bash" in x)
        file.close()

    def test_ada(self):
        self.compile_file("ada", "hello.adb")
        file = open('output.txt')
        x = file.read()
        self.assertTrue("Hello Ada" in x)
        file.close()

    def test_c(self):
        self.compile_file("c", "hello.c")
        file = open('output.txt')
        x = file.read()
        self.assertTrue("Hello C" in x)
        file.close()

    def test_cpp(self):
        self.compile_file("cpp", "hello.cpp")
        file = open('output.txt')
        x = file.read()
        self.assertTrue("Hello C++" in x)
        file.close()

    def test_fortran(self):
        self.compile_file("fortran", "hello.f90")
        file = open('output.txt')
        x = file.read()
        self.assertTrue("Hello Fortran" in x)
        file.close()

    def test_go(self):
        self.compile_file("go", "hello.go")
        file = open('output.txt')
        x = file.read()
        self.assertTrue("Hello Go" in x)
        file.close()

    def test_objc(self):
        self.compile_file("objc", "hello.m")
        file = open('output.txt')
        x = file.read()
        self.assertTrue("Hello Objective C" in x)
        file.close()

    def test_objcpp(self):
        self.compile_file("objcpp", "hello.m")
        file = open('output.txt')
        x = file.read()
        self.assertTrue("Hello Objective C" in x)
        file.close()

    def test_rust(self):
        self.compile_file("rust", "hello.rs")
        file = open('output.txt')
        x = file.read()
        self.assertTrue("Hello Rust" in x)
        file.close()

    def test_windows(self):
        win_bin = 0
        self.compile_file('c', 'hello.c', 'windows')
        comm = subprocess.run("ls", shell=True, stdout=subprocess.PIPE)
        output = str(comm).split('\\n')
        for file in output:
            if 'exe' in file:
                win_bin += 1

        self.compile_file('cpp', 'hello.cpp', 'windows')
        comm = subprocess.run("ls", shell=True, stdout=subprocess.PIPE)
        output = str(comm).split('\\n')
        for file in output:
            if 'exe' in file:
                win_bin += 1

        self.compile_file('objc', 'hello.m', 'windows')
        comm = subprocess.run("ls", shell=True, stdout=subprocess.PIPE)
        output = str(comm).split('\\n')
        for file in output:
            if 'exe' in file:
                win_bin += 1

        self.compile_file('objcpp', 'hello.m', 'windows')
        comm = subprocess.run("ls", shell=True, stdout=subprocess.PIPE)
        output = str(comm).split('\\n')
        for file in output:
            if 'exe' in file:
                win_bin += 1

        self.assertTrue(win_bin == 4)

    def test_wasm(self):
        wasm_bin = 0
        self.compile_file('c', 'hello.c', 'wasm')
        comm = subprocess.run("ls", shell=True, stdout=subprocess.PIPE)
        output = str(comm).split('\\n')
        for file in output:
            print(file)
            if 'cc' in file:
                print(file)
                wasm_bin += 1

        self.compile_file('cpp', 'hello.cpp', 'wasm')
        comm = subprocess.run("ls", shell=True, stdout=subprocess.PIPE)
        output = str(comm).split('\\n')
        for file in output:
            if 'cc' in file:
                print(file)
                wasm_bin += 1

        self.compile_file('rust', 'hello.rs', 'wasm')
        comm = subprocess.run("ls", shell=True, stdout=subprocess.PIPE)
        output = str(comm).split('\\n')
        for file in output:
            if 'cr' in file:
                print(file)
                wasm_bin += 1

        print(wasm_bin)
        subprocess.run("rm c* output.txt", shell=True)
        self.assertTrue(wasm_bin == 5)


if __name__ == '__main__':

    unittest.main()
