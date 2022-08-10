from flask import Flask, render_template, request, send_file
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import time
app = Flask(__name__)

PEOPLE_FOLDER = os.path.join('static')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html'), 500


@app.route('/download')
def downloadFile():
    path = "answer.txt"
    return send_file(path, as_attachment=True)


@app.route('/', methods=['POST', 'GET'])
def index():
    f = open('answer.txt', 'w')
    f.close()

    if request.form.get('Gauss'):
        title_text_file = request.files['file_elem']
        jptr_text_file = request.files['file_jptr']
        iptr_text_file = request.files['file_iptr']
        b_text_file = request.files['file_b']

        if title_text_file.filename == '':
            title = request.form['title']

        else:
            title = title_text_file.read()
            title = str(title, 'utf-8')

        if jptr_text_file.filename == '':
            jptr_text = request.form['jptr']
        else:
            jptr_text = jptr_text_file.read()
            jptr_text = str(jptr_text, 'utf-8')

        if iptr_text_file.filename == '':
            iptr_text = request.form['iptr']
        else:
            iptr_text = iptr_text_file.read()
            iptr_text = str(iptr_text, 'utf-8')

        if b_text_file.filename == '':
            b_text = request.form['b']
        else:
            b_text = b_text_file.read()
            b_text = str(b_text, 'utf-8')

        w = request.form['w']
        Accuracy = request.form['e']
        Accuracytext = Accuracy

        elem = [float(x) for x in title.split()]
        jptr = [int(x) for x in jptr_text.split()]
        iptr = [int(x) for x in iptr_text.split()]
        b = [float(x) for x in b_text.split()]
        n = len(iptr)-1
        diag = np.zeros(n)
        x = np.zeros(n)
        N = 500
        epsarray = np.zeros(N)
        x1_grafic = np.zeros(N)
        x2_grafic = np.zeros((N,n))
        startTime = time.time()
        k = 0
        check = False

        while check == False:
            eps = 0.0

            for i in range(n):
                d = 0.0
                for j in range(iptr[i], iptr[i + 1]):
                    if i == jptr[j]:
                        diag[i] = elem[j]
                        continue
                    d += elem[j] * x[jptr[j]]
                dx = (-d + b[i]) / diag[i]
                epsarray[k]=eps
                eps += abs(dx - x[i])
                x2_grafic[k][i] = x[i]
                x1_grafic[k] = k
                x[i] = dx
            k += 1

            if eps < float(Accuracy):
                check = True

            if k > N:
                check = True

        endTime = time.time()
        totalTime = endTime - startTime
        totalTime = float("{0:.3f}".format(totalTime))
        f = open('answer.txt', 'w')
        f.write(str(x))
        f.close()
        x3_grafic = np.zeros(k)
        epsarray2 = np.zeros(k)
        x4_grafic = np.zeros((k, n))

        for i in range(k):
            x3_grafic[i]=x1_grafic[i]
            epsarray2[i]=epsarray[i]
            for j in range(n):
                x4_grafic[i][j]=x2_grafic[i][j]

        if n < 2000:
            plt.figure(1)
            plt.plot(x3_grafic, x4_grafic)
            plt.savefig('static/saved_figure.png')

        plt.figure(2)
        plt.plot(x3_grafic, epsarray2)
        plt.savefig('static/saved_figure2.png')
        plt.show()
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'saved_figure.png')
        full_filename2 = os.path.join(app.config['UPLOAD_FOLDER'], 'saved_figure2.png')
        return render_template("index.html", elem_text=str(title), jptr_text=str(jptr_text), iptr_text=str(iptr_text), b_text=str(b_text),
                               ans_text=str(x), accuracy_text=str(Accuracytext), num_iter="Количество итераций - " + str(k-1),
                               w_text=str(w), user_image = full_filename, user_image2 = full_filename2, time_text = "Время решения - " + str(totalTime) + "с")

    elif request.form.get('Jacobi'):
        title_text_file = request.files['file_elem']
        jptr_text_file = request.files['file_jptr']
        iptr_text_file = request.files['file_iptr']
        b_text_file = request.files['file_b']

        if title_text_file.filename == '':
            title = request.form['title']
        else:
            title = title_text_file.read()
            title = str(title, 'utf-8')

        if jptr_text_file.filename == '':
            jptr_text = request.form['jptr']
        else:
            jptr_text = jptr_text_file.read()
            jptr_text = str(jptr_text, 'utf-8')

        if iptr_text_file.filename == '':
            iptr_text = request.form['iptr']
        else:
            iptr_text = iptr_text_file.read()
            iptr_text = str(iptr_text, 'utf-8')

        if b_text_file.filename == '':
            b_text = request.form['b']
        else:
            b_text = b_text_file.read()
            b_text = str(b_text, 'utf-8')

        w = request.form['w']
        Accuracy = request.form['e']
        Accuracytext = Accuracy
        elem = [float(x) for x in title.split()]
        jptr = [int(x) for x in jptr_text.split()]
        iptr = [int(x) for x in iptr_text.split()]
        b = [float(x) for x in b_text.split()]

        n = len(iptr)-1
        N = 500
        epsarray = np.zeros(N)
        x1_grafic = np.zeros(N)
        x2_grafic = np.zeros((N, n))
        diag = np.zeros(n)
        x = np.zeros(n)
        y = np.zeros(n)
        k = 0
        check = False
        startTime = time.time()

        while check == False:
            eps = 0.0
            for i in range(n):
                d = 0.0
                for j in range(iptr[i], iptr[i + 1]):
                    if i == jptr[j]:
                        diag[i] = elem[j]
                        continue
                    d += elem[j] * x[jptr[j]]
                y[i] = (-d + b[i]) / diag[i]
                epsarray[k] = eps
                eps += abs(y[i] - x[i])

            for i in range(n):
                x2_grafic[k][i] = x[i]
                x1_grafic[k] = k
                x[i] = y[i]

            if eps < float(Accuracy):
                for i in range(n):
                    x2_grafic[k][i] = x[i]
                    x1_grafic[k] = k
                check = True

            if k > N:
                check = True
            k += 1

        endTime = time.time()
        totalTime = endTime - startTime
        totalTime = float("{0:.3f}".format(totalTime))
        f = open('answer.txt', 'w')
        f.write(str(x))
        f.close()
        x3_grafic = np.zeros(k)
        epsarray2 = np.zeros(k)
        x4_grafic = np.zeros((k, n))

        for i in range(k):
            x3_grafic[i] = x1_grafic[i]
            epsarray2[i] = epsarray[i]
            for j in range(n):
                x4_grafic[i][j] = x2_grafic[i][j]

        if n < 2000:
            plt.figure(1)
            plt.plot(x3_grafic, x4_grafic)
            plt.savefig('static/saved_figure.png')

        plt.figure(2)
        plt.plot(x3_grafic, epsarray2)
        plt.savefig('static/saved_figure2.png')
        plt.show()
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'saved_figure.png')
        full_filename2 = os.path.join(app.config['UPLOAD_FOLDER'], 'saved_figure2.png')
        return render_template("index.html", elem_text=str(title), jptr_text=str(jptr_text), iptr_text=str(iptr_text),
                               b_text=str(b_text),
                               ans_text=str(x), accuracy_text=str(Accuracytext), num_iter="Количество итераций - " + str(k-1),
                               w_text=str(w), user_image=full_filename, user_image2=full_filename2, time_text = "Время решения - " + str(totalTime) + "с")

    elif request.form.get('Relax'):
        title_text_file = request.files['file_elem']
        jptr_text_file = request.files['file_jptr']
        iptr_text_file = request.files['file_iptr']
        b_text_file = request.files['file_b']

        if title_text_file.filename == '':
            title = request.form['title']

        else:
            title = title_text_file.read()
            title = str(title, 'utf-8')

        if jptr_text_file.filename == '':
            jptr_text = request.form['jptr']
        else:
            jptr_text = jptr_text_file.read()
            jptr_text = str(jptr_text, 'utf-8')

        if iptr_text_file.filename == '':
            iptr_text = request.form['iptr']
        else:
            iptr_text = iptr_text_file.read()
            iptr_text = str(iptr_text, 'utf-8')

        if b_text_file.filename == '':
            b_text = request.form['b']
        else:
            b_text = b_text_file.read()
            b_text = str(b_text, 'utf-8')

        w = request.form['w']
        Accuracy = request.form['e']
        Accuracytext = request.form['e']
        elem = [float(x) for x in title.split()]
        jptr = [int(x) for x in jptr_text.split()]
        iptr = [int(x) for x in iptr_text.split()]
        b = [float(x) for x in b_text.split()]
        n = len(iptr) - 1
        diag = np.zeros(n)
        x = np.zeros(n)
        N = 500
        epsarray = np.zeros(N)
        x1_grafic = np.zeros(N)
        x2_grafic = np.zeros((N, n))
        k = 0
        check = False
        startTime = time.time()

        while check == False:
            eps = 0.0
            for i in range(n):
                d = 0.0
                for j in range(iptr[i], iptr[i + 1]):
                    if i == jptr[j]:
                        diag[i] = elem[j]
                        continue
                    d += elem[j] * x[jptr[j]]
                dx = (-d + b[i]) / diag[i]
                epsarray[k] = eps
                eps += abs(dx - x[i])
                x2_grafic[k][i] = x[i]
                x1_grafic[k] = k
                x[i] = float(w) * dx + (1 - float(w)) * x[i]


            if eps < float(Accuracy):
                for i in range(n):
                    x2_grafic[k][i] = x[i]
                    x1_grafic[k] = k
                check = True

            if k > N:
                check = True
            k += 1

        endTime = time.time()
        totalTime = endTime - startTime
        totalTime = float("{0:.3f}".format(totalTime))
        f = open('answer.txt', 'w')
        f.write(str(x))
        f.close()
        x3_grafic = np.zeros(k)
        epsarray2 = np.zeros(k)
        x4_grafic = np.zeros((k, n))

        for i in range(k):
            x3_grafic[i] = x1_grafic[i]
            epsarray2[i] = epsarray[i]
            for j in range(n):
                x4_grafic[i][j] = x2_grafic[i][j]

        if n < 2000:
            plt.figure(1)
            plt.plot(x3_grafic, x4_grafic)
            plt.savefig('static/saved_figure.png')

        plt.figure(2)
        plt.plot(x3_grafic, epsarray2)
        plt.savefig('static/saved_figure2.png')
        plt.show()
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'saved_figure.png')
        full_filename2 = os.path.join(app.config['UPLOAD_FOLDER'], 'saved_figure2.png')
        return render_template("index.html", elem_text=str(title), jptr_text=str(jptr_text), iptr_text=str(iptr_text),
                               b_text=str(b_text), ans_text=str(x), accuracy_text=str(Accuracytext), num_iter="Количество итераций - " + str(k-1),
                               w_text=str(w), user_image=full_filename, user_image2=full_filename2, time_text = "Время решения - " + str(totalTime) + "с")

    elif request.form.get('Generation'):
        n = 0
        N = request.form['size']
        N = int(N)
        elem = np.zeros(int(N) * 2-1)
        i = 0

        while i < N + n:
            elem[i] = random.randint(40, 100)
            i = i + 1
            if i < N + n:
                n = n + 1
                elem[i] = random.randint(1, 10)
            i = i + 1

        jptr = np.zeros(N * 2)
        jptrn = 0

        for i in range(N + n):
            if elem[i] < 30:
                jptr[i] = random.randint(0, N-1)
                jptrn = jptrn + 1
            else:
                jptr[i] = i - jptrn

        iptr = np.zeros(N)
        m = 0
        m1 = 0

        for i in range(N + n):
            m = m + 1
            if jptr[i + 1] <= jptr[i]:
                iptr[m1] = m
                m1 = m1 + 1

        iptr = np.insert(iptr, 0, 0)
        b = np.zeros(N)
        for i in range(N):
            b[i] = random.randint(0, 100)

        jptr_text = np.zeros(N + n)

        for i in range(N + n):
            jptr_text[i] = jptr[int(i)]

        gen_elem = ''

        for i in range(N + n):
            gen_elem = gen_elem + " " + str(elem[i])

        jptr_text = jptr_text.astype(int)
        iptr = iptr.astype(int)
        gen_jptr = ''

        for i in range(N + n):
            gen_jptr = gen_jptr + " " + str(jptr_text[i])

        gen_iptr = ''

        for i in range(N + 1):
            gen_iptr = gen_iptr + " " + str(iptr[i])

        gen_b = ''

        for i in range(N):
            gen_b = gen_b + " " + str(b[i])

        return render_template("index.html", elem_text=str(gen_elem), jptr_text=str(gen_jptr), iptr_text=str(gen_iptr),
                               b_text=str(gen_b), size_text=str(N))
    else:
        return render_template("index.html")

if __name__== "__main__":
    app.run()

