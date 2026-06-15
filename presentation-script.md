# Presentation Script

### Title Slide

Welcome to the presentation on the design and characterization of a precision motion system, developed as a project for the course Design of Precision Engineering.

### Project Objectives

This presentation is divided into two independent sections, both related to precision motion systems.

The first section focuses on the design of a precision motion de-amplifier, while the second section focuses on the static calibration of an existing precision motion amplifier.

## Design a Precision Motion De-Amplifier

### Design Workflow

This slide summarizes the workflow followed during the design phase.

Starting from the customer need, we first defined the product and translated the requirements into engineering specifications using QFD.

Then, we improved our knowledge of the topic by decomposing the system into atomic functions. Starting from these functions, we generated possible solutions using two complementary approaches: morphological combination and TRIZ.

After that, the generated concepts were compared through a robust decision-making process, based on belief maps and a decision matrix. Finally, the selected concept was developed into an engineering model.

### Product Definition

In the product definition phase, we identified the main needs that the system had to satisfy.

The mechanism had to provide straight input and output motion, with a de-amplification ratio of one to twenty. The relation between input and output also had to be as linear as possible, with a maximum deviation of five percent, and the motion transmission had to be reversible.

The customer request also included some application constraints. The input stroke had to remain below ten millimeters, while the input force had to be lower than zero point one newtons. The mechanism also had to fit inside a space envelope of two hundred by two hundred by twenty millimeters. In addition, the output had to provide a flat sensing surface of at least five by five millimeters, and the whole system had to be supported through a Kelvin clamp.

### QFD

After defining the product, we used the QFD methodology to organize the customer request and translate it into design information.

In particular, the customer needs were first expressed as requirements, in a form that is still understandable from the customer point of view. Then, these requirements were translated into specifications, which are more directly usable in engineering design.

The QFD methodology will not be explained in detail here, since it was already presented in a previous lecture.

### Product Decomposition

The next step was product decomposition. In this phase, existing systems were analyzed and decomposed into their atomic functions.

This work was performed independently by each group member, so that different examples and different interpretations could be considered.

Product decomposition was not only useful for identifying the basic functions of the system. It was also important for improving our understanding of the topic, because it allowed us to study how similar precision mechanisms are organized and how they achieve their motion behavior.

On the right, one example of this decomposition is shown. First, the system was analyzed as a whole, looking at its degrees of freedom and its general motion behavior. Then, it was split into different elementary functions, each one associated with specific components of the system.

### Functional Decomposition

Starting from the system requirements and from the knowledge obtained through product decomposition, a functional architecture was derived.

The purpose of this architecture is to clarify which functions the system must perform, independently from the specific physical solution that will be used later.

The diagram is organized hierarchically. It starts from the main function, which represents the whole system: the linear rectilinear reversible actuator. This main function is then divided into several functions that describe the general functionalities required from the mechanism. When needed, these functions are further divided into more elementary and specific functions. In this representation, the blue blocks correspond to the higher-level functions, while the white blocks correspond to the more elementary ones.

For example, one main function is to provide the gain of one to twenty. Another example is the frame, which is one member of the system. Its function is split into two more specific functionalities: providing the preload force and avoiding misalignment between the input and output directions.

### Morphological Combination

After the functional decomposition, a morphological map was designed.

This map describes, at a conceptual level, the connections between the different atomic functions. For example, the unidirectional translation is strictly related to the reversible gain of one to twenty, while the input and output systems are connected to the unidirectional translation.

From the map, it is also possible to see an important design choice for obtaining a reversible system: the architecture should be symmetric from the point of view of the atomic functions.

However, this map does not represent the final implementation architecture. Its purpose is to identify how the functions are related to each other. After this step, the functions and their connections can be implemented through one or more physical solutions.

### TRIZ

TRIZ, the Theory of Inventive Problem Solving, was used as a second method for concept generation.

The purpose of this methodology is to solve engineering contradictions. The process starts by identifying a contradiction in the design problem. Then, this specific contradiction is abstracted into a more general problem.

At this point, the 40 TRIZ inventive principles can be used to suggest possible solution strategies. Finally, the selected strategy has to be translated back into a practical implementation for the specific system.

In our case, TRIZ was applied to solve some contradictions between the system requirements, so it helped generate additional design directions starting from the constraints of the problem.

### Example of Contradiction Resolution

This slide shows one example of how TRIZ was applied.

In the lower-left box, the real design problem is shown. The objective was to improve the reversibility of the input-output relation while preserving the small envelope dimensions of the mechanism.

This real problem was then translated into the TRIZ domain, as shown in the upper-left box. In general terms, the contradiction becomes improving the use of energy by the moving object, while preserving the volume of the moving object.

Using the TRIZ principles, the suggested typical solution was principle number 13: "the other way round". In our case, this idea was interpreted as using structural symmetry in the mechanism. Therefore, as shown in the lower-right box, if the mechanism is structurally symmetric, inverse functioning is allowed without changing the overall system dimensions.

### Concepts Generation

In this phase, the previous analyses were used to generate possible concepts for the system.

In particular, product decomposition provided a knowledge base, while the morphological map helped translate the atomic functions and their connections into different conceptual solutions.

At this stage, the focus was mainly on the system architecture, rather than on detailed implementation. However, preliminary calculations and simulations were still used to check whether the concepts were realistic and compatible with the main requirements.

The number of generated concepts was intentionally balanced: large enough to explore different engineering solutions, but limited enough to maintain a clear overview and make the comparison manageable.

As mentioned in the note, each figure in the following slides is labeled above with its corresponding concept number.

### Single-Stage Mechanical Concept

The first concept is a single-stage mechanical solution based on gears.

In this case, the motion transmission and the required gain are obtained directly through the gear ratio. The input motion is converted into the rotation of the first gear, and the second gear transfers the motion to the output side with the desired reduction ratio.

From a conceptual point of view, this solution is simple and easy to understand. However, it is not very suitable for a high-precision application, because gear mechanisms introduce backlash, friction, and contact-related errors.

### Multi-Stage Compliant Mechanism Concepts

The next concepts are based on compliant mechanisms and use a multi-stage architecture.

Here, the motion is transmitted through elastic deformation. This is important because elastic deformation can provide high repeatability and avoids problems such as backlash and friction.

The general idea is to separate the system into different stages. Some stages guide the rectilinear motion by relying on structural geometric symmetry, while another stage provides the amplification or de-amplification through lever mechanisms. The lever kinematics also helps obtain an approximately linear input-output relation.

Another important aspect is the symmetry between the input and output sides. This symmetry is used to make the mechanism reversible, so that the same architecture can work consistently in both motion directions.

### Single-Stage Compliant Mechanism Concepts

The following concepts are also based on compliant mechanisms, but they use a single-stage architecture.

In this case, the objective is to integrate motion transmission and de-amplification in the same mechanism, instead of separating them into multiple stages. The design logic is therefore more compact, while still relying on the same principles: flexure hinges, elastic deformation, lever effects, and structural geometric symmetry.

The two concepts shown in this slide propose different ways to arrange the flexure elements and the input-output path. In both cases, the goal is to obtain the required ratio while keeping the motion guided and repeatable.

### Single-Stage Compliant Mechanism Concepts

This slide shows two additional single-stage compliant concepts.

Again, the main design idea is to combine the required motion ratio, the rectilinear guidance, and the compliant transmission into one integrated architecture. The concepts differ mainly in the arrangement of the flexure hinges and the lever arms.

### Robust Decision-Making

After generating the concepts, a robust decision-making process was used to compare them.

The system requirements were adopted as decision criteria, so each concept was evaluated according to how well it could satisfy the main design needs.

The belief maps were used by each group member to evaluate the capability of each concept to satisfy the design criteria.

The results were then collected in the decision matrix. Each criterion was assigned a weight, and each concept received a score for that criterion. The final satisfaction value made it possible to rank the concepts and compare them in a structured way.

### Selected Concept

Based on the decision matrix, Concept II was selected.

This concept is a single-stage compliant mechanism, so it integrates motion transmission and de-amplification in one compact architecture. It was selected because it showed the best overall satisfaction value.

After the selection, this concept was further analyzed and developed into the final engineering model.

### Modeling Workflow

After selecting the concept, the next step was to develop it into a more detailed model.

The modeling phase started from the kinematic design, where the main motion behavior and the lever-based architecture were defined. Then, the dynamic design and the material selection were developed in parallel, because the elastic behavior of the mechanism depends strongly on both geometry and material properties.

Finally, these choices were combined and verified through simulations, in order to evaluate the performance of the final model with respect to the original design requirements.

### Kinematic Design

From a kinematic point of view, the mechanism is based on a lever architecture.

The levers are used to obtain the required linear displacement de-amplification, so that a larger input displacement produces a smaller output displacement with the target ratio.

The same architecture also supports reversible kinematic behavior, because the input and output sides are arranged in a symmetric way.

In addition, the straight-line motion is ensured by the structural symmetry of the mechanism, which helps guide the motion and reduce unwanted rotations or misalignments.

### Dynamic Design

The dynamic design was mainly based on the use of elastic deformation.

This is one of the main advantages of compliant mechanisms: the motion is obtained through elastic deformation instead of conventional mechanical joints. As a result, backlash and friction are not present, and the system can achieve high repeatability and reversible behavior.

To implement the joints, flexure hinges were adopted. Different hinge geometries were analyzed through analytical models and parametric studies.

The optimization had to balance several criteria: maximizing the allowable flexure angle, minimizing stiffness, avoiding material yielding, maintaining manufacturability, and respecting the validity range of the analytical models.

In the final design, leaf-spring hinges and circular hinges were both used. Leaf hinges provide low stiffness and large angular excursion, while circular hinges are stiffer but provide more precise motion. Combining them allowed us to balance compliance, precision, and rotational capability.

This optimization process was useful not only to improve the final design, but also to better understand the practical trade-offs involved in compliant mechanism design.

### Material Selection

The material selection was supported by the Ashby map shown in the slide.

Since the mechanism works through elastic deformation, a key requirement was high yield strength. The material had to allow the flexure hinges to deform without entering the plastic region.

For this reason, Beryllium-Copper was selected. It provides a good combination of elastic behavior and high yield strength, which helps avoid permanent deformation during operation.

### Simulation Results

This slide summarizes the main simulation results and compares them with the original design requirements.

The output-input plot shows that the simulated behavior is very close to the ideal linear interpolation. At the maximum input displacement of ten millimeters, the mechanism reaches the required gain of one to twenty.

The maximum deviation from linearity is about zero point seven percent, corresponding to zero point zero zero three five millimeters. This is well below the maximum allowed deviation of five percent, so the linearity requirement is satisfied.

The space envelope is also within the required limits, with dimensions of about one hundred ninety-nine point five by one hundred seventy-four point nine by eight millimeters.

The only value that does not satisfy the original target is the maximum input force, which is about one point zero seven newtons instead of zero point one newtons. However, this force is still relatively small in absolute terms.

Overall, the performance remains positive because the output-input ratio satisfies the specification, the behavior is highly linear, and the spatial dimensions remain within the required limits.

As reported in the note, the linearity deviation is calculated over the full-scale output range, by comparing the simulated displacement with the ideal interpolated displacement.

### Simulation Results

The second simulation slide shows the frequency response of the mechanism.

At low frequency, the system behaves as an attenuator, consistently with the de-amplification function of the mechanism.

A resonance appears at about thirty radians per second, which corresponds to approximately four point seven seven hertz. After this resonance, the magnitude decreases strongly, showing a strong post-resonance attenuation, and the phase plot shows a phase delay after resonance.

## Static Calibration of a Precision Motion Amplifier

This second part of the presentation is independent from the previous design activity.

The objective is to calibrate an existing precision motion system. In particular, the goal is to characterize the static relation between the input and output displacements.

### Measured System and Experimental Setup

This slide shows the measured system and the experimental setup used for the calibration.

The mechanism was mounted on a passive vibration-isolation bench, in order to reduce external disturbances during the measurements.

The system was positioned through a Kelvin-clamp precision mounting, with a tension spring used for attachment. The input displacement was applied manually through a precision screw, while the input and output displacements were measured using LIF sensors.

### Effect of Noise

Before performing the calibration, the effect of noise was evaluated.

The plots show the sensor drift and the stochastic noise contribution for both input and output measurements. The sensor drift is on the order of units of nanometers per second, while the stochastic contribution is on the order of tens of nanometers, with a ninety-five percent confidence level.

The noise contribution was considered negligible because its magnitude is much smaller than the operating displacement levels. In particular, the operating displacements are on the order of millimeters for the input and hundredths of millimeters for the output, while the noise is on the nanometer scale.

For this reason, additional analyses such as ACF and FFT were considered unnecessary for this calibration.

### Static Calibration Results

For the static calibration, a second-order model was adopted to fit the measured data.

The model includes an offset term, a direction-dependent term to account for forward and backward motion, a linear coefficient, and a quadratic coefficient.

The table reports the estimated regression coefficients together with their standard errors. The dominant term is the linear coefficient, while the quadratic contribution is very small.

Residual normality was checked with the Shapiro-Wilk test, obtaining a p-value of zero point fifteen. The maximum deviation from linearity is also very low, equal to zero point zero one percent.

As in the modeling section, the deviation from linearity is calculated over the full-scale output range, by comparing the measured displacement with the fitted calibration model.

### Calibration Conclusions

These two plots summarize the main calibration results.

On the left, the input-output relation is shown for both backward and forward motion. The points are very close to the fitted line, confirming the high linearity of the calibration model.

On the right, the residuals are plotted as a function of the output displacement. Their magnitude is very small, and the forward and backward measurements remain close to each other.

This confirms that the system has limited hysteresis effects and that the calibration model provides a highly linear description of the input-output relation.

### AI Usage

AI-based tools were used only as support tools during the preparation of the presentation.

In particular, ChatGPT was used for language refinement, layout optimization, and visual content support.

All generated materials were reviewed and validated by the authors.

## Thank You for Your Attention

Thank you for your attention.
