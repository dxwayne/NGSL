=======================
Astrophysics Crib Sheet
=======================

Wavelength (:math:`\lambda`) is related to frequency (:math:`\nu` nu not v) by the speed
of light (:math:`c`) :

.. math::

   \nu &= c/\lambda 

Energy (:math:`E`) of a photon (:math:`\gamma`)  given its frequency (:math:`\nu`) .

.. math::
   E_{\gamma} = \frac{h}{\nu}

Statistics:
###########

Many small cameras (if the pixels are small you need to pay
attention), have well-depths that are less than :math:`2^{16}-1=`
65,535. They will use a gain of :math:`<1` such that when divided into
the well-depth it will **fluff** the electron counts up. You need
10,000 electrons to achieve a 1% result. To first order (back-of-the-envelope)
a count of 10,000 electrons will have :math:`sigma_k =\sqrt{10,000} = 100`.

A well depth of 18,000 electrons needs GAIN = :math:`65,535/18,000 = 3.6408`.
Thus you will need :math:`10,000 \times 3.6408 = 36408` to achieve that
result. For an 1800 second exposure that produces counts on order
of 12,500 you need an accumulated exposure time of :math:`36408/12,500 = 2.9`
or 3 = (1 + 2 more) exposures.

   .. % (iv (setq GAIN (/ 65535.0 18000.0 )))   3.640833333333333
   .. % (iv (setq COUNT (* 10000.0 GAIN )))    36408.33333333333
   .. % (iv (setq BOOST (/ 36408.0  12500.0)))    2.91264
