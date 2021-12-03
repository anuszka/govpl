load 'data_dir.gp'

set fit errorvariables

filename = sprintf(ddir."/age_group%d.tsv", age_group)

a=1.
b=1e3
A = 1e-1
# y0 = 27.
c= 1e6
f(x,y)= a*x**2. +b*x+ c + A*(y-y0)**2. 
 
fit [2010:2019] f(x,y)  filename u 1:2:3 via a,b,c, A,y0

plot_title  = sprintf("%d - %d years", age_group, age_group+4)

if (age_group == 0) {
    plot_title  = sprintf("<5 years")
    } 
    
if (age_group == 90) {
    plot_title  = sprintf(">90 years")
    }

set title plot_title
set xlabel 'Year'
set ylabel 'Week'
set zlabel 'Deaths'

stats filename using 3

splot [2000:2020][0:54][0:STATS_max] f(x,y) title 'Trend 2000-2019', filename u 1:2:3 with lines title 'Data'

set print ddir."/fit_parameters.csv" append
print age_group, ",", a,",",a_err,",", b,",",b_err,",", c, ",",c_err,",", A,",", A_err, "," , y0, "," , y0_err
set print
