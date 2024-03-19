# Sparcle: Boosting the Accuracy of Data Cleaning Systems through Spatial Awareness

This is an implementation of Sparcle ideas in side Baran system (Raha 1.25). 

The implementation is in branch "sparcle", in file [raha/correction.py](https://github.com/yhuang-db/baran-sparcle/blob/sparcle/raha/correction.py#).

The best way to understand the implementation is to [compare the sparcle-version (branch sparcle) with the original version (branch main)](https://github.com/yhuang-db/baran-sparcle/compare/main...sparcle#diff-14b16ec8041e13629779f3d87c33456f6ea0742e1258545658da80992c3c34c0R210), where the original function "_to_model_adder" adds 1 to a specific location (i.e., "key" in "model[key][value]+=1.0"), sparcle function "_sparcle_to_model_adder" also adds **weight** to neightborhood locations. 

<img width="1344" alt="Screenshot 2024-03-19 at 13 13 37" src="https://github.com/yhuang-db/baran-sparcle/assets/42155071/f45fea8b-1aea-4a04-a928-aef9f9578c5b">


The experiment and driver code is in [raha/sparcle_exp_driver.py](https://github.com/yhuang-db/baran-sparcle/blob/sparcle/raha/sparcle_exp_driver.py).
