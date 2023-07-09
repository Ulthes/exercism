"""Functions to prevent a nuclear meltdown."""


def is_criticality_balanced(temperature, neutrons_emitted):
    """Verify criticality is balanced.

    :param temperature: int or float - temperature value in kelvin.
    :param neutrons_emitted: int or float - number of neutrons emitted per second.
    :return: bool - is criticality balanced?

    A reactor is said to be critical if it satisfies the following conditions:
    - The temperature is less than 800 K.
    - The number of neutrons emitted per second is greater than 500.
    - The product of temperature and neutrons emitted per second is less than 500000.
    """
    safe_temperature: int = 800
    safe_neutrons_number: int = 500
    safe_product_multiplication: int = 500000
    is_current_temperature_critical: bool = temperature < safe_temperature
    is_current_neutrons_critical: bool = neutrons_emitted > safe_neutrons_number
    is_product_critical: bool = temperature * neutrons_emitted < safe_product_multiplication
    return is_current_temperature_critical and is_current_neutrons_critical and is_product_critical


def reactor_efficiency(voltage, current, theoretical_max_power):
    """Assess reactor efficiency zone.

    :param voltage: int or float - voltage value.
    :param current: int or float - current value.
    :param theoretical_max_power: int or float - power that corresponds to a 100% efficiency.
    :return: str - one of ('green', 'orange', 'red', or 'black').

    Efficiency can be grouped into 4 bands:

    1. green -> efficiency of 80% or more,
    2. orange -> efficiency of less than 80% but at least 60%,
    3. red -> efficiency below 60%, but still 30% or more,
    4. black ->  less than 30% efficient.

    The percentage value is calculated as
    (generated power/ theoretical max power)*100
    where generated power = voltage * current
    """

    generated_power: int = voltage * current
    efficiency: int = (generated_power / theoretical_max_power) * 100
    is_efficiency_green: bool = efficiency >= 80
    is_efficiency_orange: bool = 80 > efficiency >= 60
    is_efficiency_red: bool = 60 > efficiency >= 30

    if is_efficiency_green:
        return "green"
    if is_efficiency_orange:
        return "orange"
    if is_efficiency_red:
        return "red"
    return "black"


def fail_safe(temperature, neutrons_produced_per_second, threshold):
    """Assess and return status code for the reactor.

    :param temperature: int or float - value of the temperature in kelvin.
    :param neutrons_produced_per_second: int or float - neutron flux.
    :param threshold: int or float - threshold for category.
    :return: str - one of ('LOW', 'NORMAL', 'DANGER').

    1. 'LOW' -> `temperature * neutrons per second` < 90% of `threshold`
    2. 'NORMAL' -> `temperature * neutrons per second` +/- 10% of `threshold`
    3. 'DANGER' -> `temperature * neutrons per second` is not in the above-stated ranges
    """
    current_power: float = temperature * neutrons_produced_per_second
    is_current_power_low: bool = current_power < threshold * 0.9
    is_current_power_normal: bool = threshold * 0.9 <= current_power <= threshold * 1.1

    if is_current_power_low:
        return "LOW"
    if is_current_power_normal:
        return "NORMAL"
    return "DANGER"
