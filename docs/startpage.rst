blackbox.StartPage
==================

.. warning:: This section is under construction.

.. py:class:: StartPage(tk.Frame) 

    Initializes the main menu page with four options.

    :param tk.Frame: Tkinter frame

    .. py:data:: Label
        :type: tk.Label

        ``Main Menu``

    .. py:data:: Button1
        :type: ttk.Button
        
        ``New Experiment``
        
        Navigates to *ExpSelPg*.
        Command: show_frameAlpha()

    .. py:data:: Button2
        :type: ttk.Button

        ``Data Menu``
        
        Navigates to *Data Menu*.
        See :doc:`analysis` for detailed instructions.

    .. py:data:: Button3
        :type: ttk.Button

        ``Preview Camera``
        
        Navigates to *CameraPreviewPg*.
        Command: show_frameSquid()

    .. py:data:: Button4
        :type: ttk.Button

        ``Quit``
        
        Exits the program.

    .. py:method:: __init__(parent, controller)

        Initializes UI elements.
    
