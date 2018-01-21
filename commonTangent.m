(* ::Package:: *)

(* ::Input:: *)
(*SetDirectory["/Volumes/MicroSD/2_PostDoc_SD/CaCO3/Common_Tangent-master"]*)
(*oneDat=Import["1.dat"][[2;;-1]]*)
(*twoDat=Import["2.dat"][[2;;-1]]*)


(* ::Input:: *)
(*Show[ListLinePlot@{oneDat,twoDat},ListPlot@{oneDat,twoDat}]*)


(* ::Input:: *)
(*ClearAll@x*)


(* ::Input:: *)
(*fitOneDatx=Fit[oneDat,{1,x,x^2,x^3},x]*)
(*fitTwoDatx=Fit[twoDat,{1,x,x^2,x^3},x]*)
(*fitOneDat=fitOneDatx/.x->y*)
(*fitTwoDat=fitTwoDatx/.x->z*)


(* ::Input:: *)
(*Show[ListPlot[{oneDat,twoDat},PlotLegends->{"OneDat","TwoDat"}],Plot[fitOneDatx,{x,55,68},PlotStyle->Directive[Dashing[0.02],Red],PlotLegends->{"OneDatFit"}],Plot[fitTwoDatx,{x,55,68},PlotStyle->Directive[Dashing[0.02],Green],PlotLegends->{"TwoDatFit"}],ImageSize->1000]*)


(* ::Input:: *)
(*fitOneDat*)
(*fitOneDatDash=D[fitOneDat,y]*)
(*fitTwoDat*)
(*fitTwoDatDash=D[fitTwoDat,z]*)


(* ::Input:: *)
(*sol=Solve[{(fitOneDat-fitTwoDat)/(y-z)==fitTwoDatDash&&(fitOneDat-fitTwoDat)/(y-z)==fitOneDatDash},{y,z},Reals]*)
(*solConditions=Solve[{(fitOneDat-fitTwoDat)/(y-z)==fitTwoDatDash&&(fitOneDat-fitTwoDat)/(y-z)==fitOneDatDash&&56<z<64&&56<y<64},{y,z},Reals]*)


(* ::Input:: *)
(*solConditions[[2]]*)


(* ::Input:: *)
(*a=fitTwoDat/.solConditions[[2]]*)
(*b=-fitOneDatDash*z/.solConditions[[2]]*)
(*c=(fitOneDatDash/.solConditions[[2]])*x*)
(*commonTangent=a+b+c*)


(* ::Input:: *)
(*Show[ListPlot[{oneDat,twoDat}],Plot[{fitOneDatx,fitTwoDatx,commonTangent},{x,55,68}],ImageSize->800]*)
