create table
  public.cart_items (
    cart_id bigint generated by default as identity,
    part_id bigint not null,
    quantity bigint null,
    id bigint generated by default as identity,
    constraint cart_items_pkey primary key (id),
    constraint cart_items_cart_id_fkey foreign key (cart_id) references carts (cart_id),
    constraint cart_items_part_id_fkey foreign key (part_id) references part_inventory (part_id)
  ) tablespace pg_default;

  create table
  public.carts (
    cart_id bigint generated by default as identity,
    user_id bigint not null,
    created_at timestamp with time zone not null default (now() at time zone 'utc'::text),
    constraint cart_table_pkey primary key (cart_id),
    constraint carts_user_id_fkey foreign key (user_id) references users (id)
  ) tablespace pg_default;

  create table
  public.case_specs (
    id bigint generated by default as identity,
    part_id bigint null,
    name text not null,
    type text null,
    color text null,
    psu text null,
    side_panel text null,
    external_volume text null,
    internal_35_bays bigint null,
    constraint case_specs_pkey primary key (id),
    constraint case_specs_part_id_fkey foreign key (part_id) references part_inventory (part_id) on update cascade
  ) tablespace pg_default;

  create table
  public.cpu_specs (
    id bigint generated by default as identity,
    part_id bigint null,
    name text null,
    core_count integer null,
    core_clock real null,
    boost_clock real null,
    tdp integer null,
    graphics text null,
    smt boolean null,
    constraint cpu_specs_pkey primary key (id),
    constraint cpu_specs_part_id_fkey foreign key (part_id) references part_inventory (part_id) on delete cascade
  ) tablespace pg_default;

  create table
  public.internal_hard_drive_specs (
    id bigint generated by default as identity,
    part_id bigint not null,
    name text not null,
    capacity integer not null,
    price_per_gb integer not null,
    type text not null,
    cache bigint not null,
    form_factor text not null,
    interface text not null,
    constraint storage_pkey primary key (id),
    constraint internal_hard_drive_specs_part_id_fkey foreign key (part_id) references part_inventory (part_id) on update cascade
  ) tablespace pg_default;

  create table
  public.monitor_specs (
    id bigint generated by default as identity,
    part_id bigint null,
    name text null,
    screen_size real null,
    resolution text null,
    refresh_rate integer null,
    response_time real null,
    panel_type text null,
    aspect_ratio text null,
    constraint monitor_specs_pkey primary key (id),
    constraint monitor_specs_part_id_fkey foreign key (part_id) references part_inventory (part_id) on delete cascade
  ) tablespace pg_default;

  create table
  public.motherboard_specs (
    id bigint generated by default as identity,
    part_id bigint not null,
    name text null,
    socket text null,
    form_factor text null,
    max_memory integer null,
    memory_slots integer null,
    color text null,
    constraint motherboard_specs_pkey primary key (id),
    constraint motherboard_specs_part_id_fkey foreign key (part_id) references part_inventory (part_id) on delete cascade
  ) tablespace pg_default;

  create table
  public.part_inventory (
    part_id bigint generated by default as identity,
    name text null,
    type text null,
    quantity bigint null default '0'::bigint,
    price double precision null,
    constraint part_inventory_pkey primary key (part_id),
    constraint part_inventory_quantity_check check ((quantity >= 0))
  ) tablespace pg_default;

  create table
  public.pc_template_parts (
    id bigint generated by default as identity,
    template_id bigint not null,
    user_id bigint not null,
    part_id bigint not null,
    quantity integer not null,
    created_at timestamp with time zone not null default (now() at time zone 'utc'::text),
    constraint pc_template_parts_pkey primary key (id),
    constraint pc_template_parts_part_id_fkey foreign key (part_id) references part_inventory (part_id),
    constraint pc_template_parts_template_id_fkey foreign key (template_id) references pc_templates (id),
    constraint pc_template_parts_user_id_fkey foreign key (user_id) references users (id)
  ) tablespace pg_default;

  create table
  public.pc_templates (
    id bigint generated by default as identity,
    user_id bigint not null,
    created_at timestamp with time zone not null default (now() at time zone 'utc'::text),
    constraint pc_template_table_pkey primary key (id),
    constraint pc_templates_user_id_fkey foreign key (user_id) references users (id)
  ) tablespace pg_default;

  create table
  public.power_supply_specs (
    id bigint generated by default as identity,
    part_id bigint not null,
    name text null,
    type text null,
    efficiency text null,
    wattage integer null,
    modular text null,
    color text null,
    constraint power_supply_specs_pkey primary key (id),
    constraint power_supply_specs_part_id_fkey foreign key (part_id) references part_inventory (part_id) on update cascade
  ) tablespace pg_default;

  create table
  public.purchase_history (
    id bigint generated by default as identity,
    user_id bigint not null,
    created_at timestamp with time zone not null default (now() at time zone 'utc'::text),
    part_id integer not null,
    payment real not null,
    constraint purchase_history_pkey primary key (id),
    constraint purchase_history_user_id_fkey foreign key (user_id) references users (id)
  ) tablespace pg_default;

  create table
  public.users (
    id bigint generated by default as identity,
    name text not null,
    address text not null,
    phone text not null,
    email text not null,
    constraint users_pkey primary key (id)
  ) tablespace pg_default;

  create table
  public.video_card_specs (
    id bigint generated by default as identity,
    part_id bigint null,
    name text not null,
    chipset text null,
    memory bigint null,
    core_clock bigint null,
    boost_clock bigint null,
    color text null,
    length bigint null,
    constraint gpu_specs_pkey primary key (id),
    constraint video_card_specs_part_id_fkey foreign key (part_id) references part_inventory (part_id) on update cascade
  ) tablespace pg_default;