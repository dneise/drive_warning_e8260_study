# Study of FACT Drive "E8260" Problems starting April 2014

Within this little repo I try to collect everything I did during my attempts to understand what causes the "E8260" warnings created by the FACT drive system by Bosch Rexroth.

This aims to be a complete collection of the code, documentation and formerly loose files used for this study.
The input data, I used for this study is not uploaded to github but stored at the ISDC. 

So in order to clone the entire stuff to you local machine, this is recommended:

    git clone https://github.com/dneise/drive_warning_e8260_study.git
    cd drive_warning_e8260_study
    scp -r isdc:/scratch/fact/drive_warning_e8260_study_data data/.

(Assuming that your isdc hostname is set to `isdc` in your `.ssh/config`)

But you don't have to clone all this to your local machine.
In case you just want to read what I concluded, just start at the introduction (coming soon).



### update the `drive_warning_e8260_study_data` at ISDC

So hopefully I do not forget it, but whenever I update this repo on github, I also have to copy my current `data/` folder to isdc, so that you can see the same state the I see. So I don't forget it, I do it like this:

    cd drive_warning_e8260_study/data
    rsync -rv * isdc:/scratch/fact/drive_warning_e8260_study_data/.
    
