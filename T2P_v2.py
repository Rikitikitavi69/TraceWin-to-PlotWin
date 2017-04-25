import os
import pandas
import random
import time
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

gui = Tk()
gui.wm_title("TraceWin -> PlotWin converter")
gui.resizable(width=False, height=False)



#Functions
def load_file():
    fname = askopenfilename(filetypes=(("Text files", "*.txt"),("All files", "*.*")))
    text_filebrowse.delete(0, END)
    text_filebrowse.insert(0, os.path.normpath(fname))
    InputFileName0=os.path.basename(fname)
    global InputFileName
    InputFileName = os.path.splitext(InputFileName0)[0]

def open_file():
    filepath = text_filebrowse.get()
    particle_mass = float(value_P12.get())
    kinetic_energy = float(value_P13.get())
    freq = int(value_P14.get())
    spc_chrg = float(value_P15.get())
    beta = float(value_P16.get())
    #print(filepath,particle_mass,kinetic_energy,freq,spc_chrg,beta)
    #print(filepath,particle_mass,kinetic_energy,freq,spc_chrg,beta)
    df = pandas.read_table(filepath, delim_whitespace = True)
    df = df.drop(df.columns[4:8],1)
    df = df.drop(df.columns[-1:],1)
    df.iloc[:,0:4] = df.iloc[:,0:4].applymap(lambda x: float('%.10f' % (float(x)*0.001)))
    cols = ["x(mm)","x'(mrad)","y(mm)","y'(mrad)","z","dp/p"]
    df2 = pandas.DataFrame(columns = cols)
    df2 = pandas.concat([df2, df.drop(df.columns[-1:],1)])

    df_dict = df.to_dict()
    energy = df_dict['Energy(MeV)']
    dp_p = []
    for i in energy:
        dp_p_formula = ((energy[i] - kinetic_energy) / kinetic_energy) * 0.5
        dp_p.append(format(dp_p_formula, '.10f'))
    df2['dp/p'] = dp_p

    lambd = 299792458 / (freq * 1000000)
    df2["z"] = df2["z"].map(lambda x: round(random.uniform(-180,180),2) * ( (-beta * lambd) / 360))
    p11 = df2.shape[0]

    outheader = [p11, particle_mass, kinetic_energy, freq, spc_chrg,""]
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filenametoexport = timestr+'_'+InputFileName+".txt"
    df2.to_csv(filenametoexport, sep=' ', header=outheader ,encoding='utf-8', columns=cols, index=False)

def generalwork():
    open_file()
    labelText.set("Done!")

#GUI
text_P12 = Label(gui, text = "Particle mass (MeV):")
text_P12.grid(row=2,column=0)
value_P12 = StringVar()
entry_P12 = Entry(gui, textvariable=value_P12, width=40)
entry_P12.grid(row=2,column=1,columnspan=1)

text_P13 = Label(gui, text = "Kinetic energy (MeV):")
text_P13.grid(row=3,column=0)
value_P13 = StringVar()
entry_P13 = Entry(gui, textvariable=value_P13, width=40)
entry_P13.grid(row=3,column=1,columnspan=1)

text_P14 = Label(gui, text = "Frequency (MHz):")
text_P14.grid(row=4,column=0)
value_P14 = StringVar()
entry_P14 = Entry(gui, textvariable=value_P14, width=40)
entry_P14.grid(row=4,column=1,columnspan=1)

text_P15 = Label(gui, text = "Space charge:")
text_P15.grid(row=5,column=0)
value_P15 = StringVar()
entry_P15 = Entry(gui, textvariable=value_P15, width=40)
entry_P15.grid(row=5,column=1,columnspan=1)

text_P16 = Label(gui, text = "Beta:")
text_P16.grid(row=6,column=0)
value_P16 = StringVar()
entry_P16 = Entry(gui, textvariable=value_P16, width=40)
entry_P16.grid(row=6,column=1,columnspan=1)

prettyframe1 = Frame(gui, background='black',width=50)
prettyframe1.grid(row=1, column=0,sticky=W+E,columnspan=2)

prettyframe2 = Frame(gui, background='black',width=50)
prettyframe2.grid(row=7, column=0,sticky=W+E,columnspan=2)


filebrowse = Button(gui, text="Browse", command=load_file, width=10)
filebrowse.grid(row=0, column=0, sticky=W)

text_filebrowse = Entry(gui,width=40)
text_filebrowse.grid(row=0,column=1,columnspan=1)

convbut = Button(gui, text="Convert", width=10, command=generalwork)
convbut.grid(row=8, column=0, sticky=W)

labelText = StringVar()
status = Label(gui, textvariable=labelText, bd=1, relief=SUNKEN, anchor=W, width=50)
status.grid(row=10,column=0,sticky=W+E,columnspan=2)

gui.mainloop()
