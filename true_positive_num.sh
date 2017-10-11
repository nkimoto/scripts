##Usage : true_positive_num.sh AnsVCF CheckVCF

##$1 > old_ans_sample
cat $1 | while read line
do
grep -v '#' > cut -f2 
done > new_ans_sample

cat $2 | while read line
do
grep -v '#' > cut -f2
done > new_check_sample

python true_positive_num.py
