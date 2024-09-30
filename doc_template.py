def template(order_number, order_date, employees, job_date) -> str:
    return f"Приказ № 7-{order_number} от {order_date}г. Приказ о привлечении к работе " \
           f"в выходные (нерабочие, праздничные) дни работников: {employees} {job_date}г."
