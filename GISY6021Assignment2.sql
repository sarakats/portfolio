-- Function: COGS_CONVERT_UNIT
-- Purpose : To convert units of measurement based on values within the table SDO_UNIT_OF_MEASURE

create or replace function COGS_CONVERT_UNIT (
    in_value number, 
    in_unit  varchar2, 
    out_unit varchar2
    ) return number as 

    -- Declare variables to be used within function:
    unit_type_in  varchar2(25);
    unit_type_out varchar2(25);
    factor_b_in   number;
    factor_c_in   number;
    factor_b_out  number;
    factor_c_out  number;
    SI            number;
    output_value  number;

begin 
    -- Get unit types for input unit
    select unit_of_meas_type
    into   unit_type_in
    from   sdo_units_of_measure
    where  lower(unit_of_meas_name) = lower(in_unit);

    -- Get unit types for output unit
    select unit_of_meas_type
    into   unit_type_out
    from   sdo_units_of_measure
    where  lower(unit_of_meas_name) = lower(out_unit);

    -- Check if units are of same types; raise application error if not
    if unit_type_in != unit_type_out then 
        raise_application_error(-20202, 'Units must be of same type.');
    end if;

    -- Check if input units are the same, return initial value if so
    if in_unit = out_unit then 
        return in_value;
    else 
        -- Get the FACTOR_"" column values for the input unit
        select factor_b, factor_c
        into   factor_b_in, factor_c_in
        from   sdo_units_of_measure 
        where  lower(short_name) = lower(in_unit);
        
        -- Get the FACTOR_"" column values for the output unit
        select factor_b, factor_c
        into   factor_b_out, factor_c_out
        from   sdo_units_of_measure 
        where  lower(short_name) = lower(out_unit);
        
        -- Calculate the SI value based on the input unit
        SI := in_value * factor_b_in / factor_c_in;
        
        -- Convert from SI to the output unit
        output_value := SI * factor_c_out / factor_b_out;
        
        -- Return the value converted to the output unit
        return output_value;    
    end if;
end;

-- Analysis Task
-- Statement to calculate the area of potatoes grown in each province
select   p.province_name as "Province Name", cr.crop_name as "Crop Name", 
         COGS_CONVERT_UNIT((sum(f.hectares)), 'hectare', 'acre') as "Total Area (acres)"
from     province p
join     ccs c on p.province_uid = c.province_uid
join     farms f on c.ccsuid = f.ccsuid
join     crops cr on f.cropuid = cr.cropuid
where    cr.crop_name like 'Potatoes'
group by p.province_name, cr.crop_name;