blackbox.BehaviorBox
====================

.. py:class:: BehaviorBox(tk.Tk, Experiment) 

    Baseline code to initialize everything.

    :param tk.Tk: Tkinter window
    :param Experiment: Experiment class

    .. py:method:: __init__(*args, **kwargs)

        Initializes Tkinter frames, renders all pages, and raises *StartPage*. 
        
        Creates button styles and sets font sizes.
        
        :param \*args: Variable length argument list
        :param \*\*kwargs: Arbitrary keyword arguments

    .. py:method:: startfresh()

        Reinitialize page and update values. 
        Works on the following pages: *StartPage*, *ExpSelPg*, *TimeSelPg*, *ConfirmPg*, *InsertPg*, *StimPrepPg*, *DataDelPg*.

    .. py:method:: show_frame(cont)

        Raises frame ``cont`` to front.

    .. py:method:: show_frameAlpha(cont)

        Resets all variables in the *Experiment* class and reinitalizes all necessary pages to starting state. 
        Raises frame ``cont`` to front.

        Used when navigating from *StartPage* to *ExpSelPg*.

    .. py:method:: show_frameZebra(cont)

        Stops camera preview. Raises frame ``cont`` to front.

        Used when navigating from *InsertPg* to *ConfirmPg*.

    .. py:method:: show_frameFish(cont)

        Starts camera preview. Raises frame ``cont`` to front.

        Used when navigating from *ConfirmPg* to *InsertPg*.

    .. py:method:: show_frameCharlie(cont)

        Confirms labels. Raises frame ``cont`` to front.

        Used when navigating from *TimeSelPg* to *ConfirmPg*.

    .. py:method:: show_frameDelta(cont)

        Depending on the type of experiment selected, displays ready or prompts the user to insert stimuli. 
        Raises frame ``cont`` to front.

        Used when navigating from *InsertPg* to *StimPrepPg*.

    .. py:method:: show_frameEcho(cont)

        Creates a folder for experiment data and images. 
        Captures images for duration of experiment and saves images to /ExpDataPictures/image. 
        Raises frame ``cont`` to front.
        
        Sets frame rate for image capturing based on type of experiment selected.
        
        * Chemotaxis: ``fps=0.33``

        * Scrunching: ``fps=4``

    .. py:method:: show_frameFoxtrot(cont)

        Reinitalizes frame ``cont`` without prompting for confirmation.

    .. py:method:: show_frameFoxtrot2(cont)

        Prompts user for confirmation and reinitializes frame ``cont``.

    .. py:method:: show_frameLima(cont, chosenexp)

        Loads ``Momo`` object and displays first image from chosen experiment.
        Raises frame ``cont`` to front.

        Used when navigating from *DataAnalysisPg* to *DataAnalysisImagePg*.

        .. py:data:: Momo

            Global variable to store experiment object.

    .. py:method:: show_frameBean(cont)

        Displays the first picture and raises frame ``cont`` to front.

        Used when navigating from *AnalysisTypeForNone* to *DataAnalysisImagePg*.

    .. py:method:: show_frameMarlin(cont)

        Configures *ReviewData* to display all images taken during the experiment on a Tkinter canvas.
        Raises frame ``cont`` to front.

        Used when navigating from *ExpFinishPg* to *ReviewData*.

    .. py:method:: show_frameStingray(cont, obj)

        Saves ``obj`` and raises frame ``cont`` to front.

        Used when navigating from *ReviewData* to *StartPage*.

    .. py:method:: show_frameRhino(cont)

        Recursively deletes all experiment data stored in Appa.savefile and raises frame ``cont`` to front.

        Used when navigating from *ReviewData* to *StartPage*.

    .. py:method:: show_frameShark(cont)

        Checks to see if an experiment was chosen to graph and checks if the selected experiment has already been analyzed. 
        Raises frame ``cont`` to front.

        Used when navigating from *DataGraphChoice* to *GraphPage*.

    .. py:method:: show_frameSquid(cont)

        Starts camera preview and raises frame ``cont`` to front.

        Used when navigating from *StartPage* to *CameraPreviewPg*.