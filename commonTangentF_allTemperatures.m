(* ::Package:: *)

(* ::Input:: *)
(*SetDirectory["/Volumes/MicroSD/2_PostDoc_SD/CaCO3/Common_Tangent-Mathematica/TEST/Files_Outputs"]*)
(*oneDat=Import["vol_Free_allTemps_ordered_I.dat"];*)
(*twoDat=Import["vol_Free_allTemps_ordered_II.dat"];*)
(*temps=Flatten@Import["temperatures.dat"]*)


(* ::Input:: *)
(*(*30 temperatures. Each 11 for I*)*)


(* ::Input:: *)
(*oneDataParts=Table[Partition[oneDat,11][[i]],{i,1,30}];*)
(*twoDataParts=Table[Partition[twoDat,9][[i]],{i,1,30}];*)


(* ::Input:: *)
(*With[{p=30},Show[{ListLinePlot[Evaluate@Table[oneDataParts[[i]],{i,1,p}],PlotLegends->temps],ListPlot[Evaluate@Table[oneDataParts[[i]],{i,1,p}]],ListLinePlot[Evaluate@Table[twoDataParts[[i]],{i,1,p}]],ListPlot[Evaluate@Table[twoDataParts[[i]],{i,1,p}]]},PlotRange->All,Frame->True,ImageSize->900]]*)


(* ::Input:: *)
(*fitOneDatx=Table[Fit[oneDataParts[[i]],{1,x,x^2,x^3},x],{i,1,30}];*)
(*fitTwoDatx=Table[Fit[twoDataParts[[i]],{1,x,x^2,x^3},x],{i,1,30}];*)
(*fitOneDat=fitOneDatx/.x->y;*)
(*fitTwoDat=fitTwoDatx/.x->z;*)
(**)


(* ::Input:: *)
(*Show[ListPlot[{oneDataParts[[1]],twoDataParts[[1]]},PlotLegends->{"OneDat","TwoDat"}],Plot[fitOneDatx[[1]],{x,55,68},PlotStyle->Directive[Dashing[0.02],Red],PlotLegends->{"OneDatFit"}],Plot[fitTwoDatx[[1]],{x,54,68},PlotStyle->Directive[Dashing[0.02],Green],PlotLegends->{"TwoDatFit"}],ImageSize->1000]*)


(* ::Input:: *)
(*fitOneDat*)
(*fitOneDatDash=D[fitOneDat,y]*)
(*fitTwoDat*)
(*fitTwoDatDash=D[fitTwoDat,z]*)


(* ::Input:: *)
(**)


(* ::Input:: *)
(*sol=Solve[{(fitOneDat[[1]]-fitTwoDat[[1]])/(y-z)==fitTwoDatDash[[1]]&&(fitOneDat[[1]]-fitTwoDat[[1]])/(y-z)==fitOneDatDash[[1]]},{y,z},Reals]*)


(* ::Input:: *)
(*solConditions=Table[Solve[{(fitOneDat[[i]]-fitTwoDat[[i]])/(y-z)==fitTwoDatDash[[i]]&&(fitOneDat[[i]]-fitTwoDat[[i]])/(y-z)==fitOneDatDash[[i]]&&56<z<64&&56<y<64},{y,z},Reals],{i,1,30}]*)


(* ::Input:: *)
(*solConditions[[1;;18]]*)


(* ::Input:: *)
(*solConditions[[1]][[2]]*)


(* ::Input:: *)
(*a=Table[fitTwoDat[[i]]/.solConditions[[i]][[2]],{i,1,17}]*)
(*b=Table[-fitOneDatDash[[i]]*z/.solConditions[[i]][[2]],{i,1,17}]*)
(*c=Table[(fitOneDatDash[[i]]/.solConditions[[i]][[2]])*x,{i,1,17}]*)
(*commonTangent=Table[a[[i]]+b[[i]]+c[[i]],{i,1,17}]*)


(* ::Input:: *)
(*phaseBoundaryData=Transpose[{temps[[1;;17]],(c/.x->-1)*4.3597482*10^3}]*)


(* ::Input:: *)
(*phaseBoundaryData//TableForm*)


(* ::Input:: *)
(*Export["absolutePressuresMathematica.dat",phaseBoundaryData//TableForm]*)


(* ::Input:: *)
(*Show[Table[Show[ListPlot[{oneDataParts[[i]],twoDataParts[[i]]}],Plot[{fitOneDatx[[i]],fitTwoDatx[[i]],commonTangent[[i]]},{x,54,68}],ImageSize->900],{i,1,15}],PlotRange->All]*)


(* ::Input:: *)
(**)


(* ::InheritFromParent:: *)
(**)
(*ListPlot@phaseBoundaryData*)
