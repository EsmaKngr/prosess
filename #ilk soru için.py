#ilk soru için
from multiprocessing import Process, Pipe

# Child process için fonksiyon
def child_process(pipe):
    # Parent'tan gelen mesajı al
    parent_message = pipe.recv()
    print(f"Child: Parent'tan gelen mesaj -> {parent_message}")
    
    # Parent'a mesaj gönder
    pipe.send("Merhaba")

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()

    # Child process'i başlat
    child = Process(target=child_process, args=(child_conn,))
    child.start()

    # Child'a mesaj gönder
    parent_conn.send("Merhaba")
    
    # Child'dan mesaj al
    child_message = parent_conn.recv()
    print(f"Parent: Child'dan gelen mesaj -> {child_message}")
    
    child.join()
    print("Child process tamamlandı.")

#ikinci soru için
import os

def simulate_abort():
   
    print("Child: Hata  abort() çağrılıyor...")
    os.abort()  

def simulate_exit():
    
    #Temiz bir şekilde çıkış yapılmasını simüle eder.
    print("Child: İşlem sonlandırıyor... exit() çağrılıyor.")
    exit(0)  

if __name__ == "__main__":
    # abort() işlevini simüle eden child process
    pid = os.fork()
    if pid == 0:
        simulate_abort()  # Child process içindeyiz
    else:
        _, status = os.wait()  # Parent, child'ın bitmesini bekler
        print(f"Parent: Child abort ile sonlandı. Çıkış kodu: {status}")

    # exit() işlevini simüle eden child process
    pid = os.fork()
    if pid == 0:
        simulate_exit()  # Child process içindeyiz
    else:
        _, status = os.wait()  # Parent, child'ın bitmesini bekler
        print(f"Parent: Child exit ile sonlandı. Çıkış kodu: {status}")

#üçüncü soru için
import os

# 1. Child process: Dosya oluşturma
def create_file():
    print("Child 1: Dosya oluşturuluyor...")
    with open("example.txt", "w") as file:
        file.write("Bu dosya, child process tarafından oluşturuldu.\n")
    print("Child 1: Dosya oluşturuldu.")

# 2. Child process: Dosyaya veri ekleme
def write_to_file():
    print("Child 2: Dosyaya veri ekleniyor...")
    with open("example.txt", "a") as file:
        file.write("Bu dosyaya child 2 tarafından veri eklendi.\n")
    print("Child 2: Veri eklendi.")

# 3. Child process: Dosya içeriğini okuma
def read_file():
    print("Child 3: Dosya okunuyor...")
    with open("example.txt", "r") as file:
        content = file.read()
    print("Child 3: Dosya içeriği:")
    print(content)

if __name__ == "__main__":
    # Parent process, üç child process başlatacak

    # 1. Child: Dosya oluşturma
    pid1 = os.fork()
    if pid1 == 0:
        create_file()
        os._exit(0)  # Child process sonlandırılır

    # 2. Child: Dosyaya veri ekleme
    pid2 = os.fork()
    if pid2 == 0:
        write_to_file()
        os._exit(0)  # Child process sonlandırılır

    # 3. Child: Dosya içeriğini okuma
    pid3 = os.fork()
    if pid3 == 0:
        read_file()
        os._exit(0)  # Child process sonlandırılır

    # Parent process, child'ların bitmesini bekler
    os.waitpid(pid1, 0)
    os.waitpid(pid2, 0)
    os.waitpid(pid3, 0)

    print("Parent: Tüm child process'ler tamamlandı.")
